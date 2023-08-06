"""Contains the acutal sync implementation"""
import os
import shutil
import platform
import glob
import logging
import datetime
import json

import boto3
import botocore
from colorama import Style

from classes.fileinfo import FileInfo

class Glacync(object):
    """Class containing all implementation details concerning the glacier sync"""
    folder = ""
    vault_name = ""
    mode = ""
    account_id = ""
    skip = ""
    pattern = ""
    weekly_cycle = 0

    glacier = ""

    def __init__(self, folder, vault_name, mode, account_id, skip, pattern, weekly_cycle):
        self.folder = folder
        self.vault_name = vault_name
        self.mode = mode
        self.weekly_cycle = weekly_cycle
        self.account_id = account_id
        self.skip = skip
        self.pattern = pattern

        self.glacier = boto3.resource('glacier')

    def get_latest_fileinfo(self, path=''):
        """Determines the most current file in a folder"""
        if not path:
            path = self.folder

        # Sanitary work
        if not path.endswith('/'):
            path += '/'

        try:
            files = [s for s in glob.glob(path + self.pattern)
                     if os.path.isfile(os.path.join(path, s))]
            files.sort(key=lambda s: os.path.getmtime(os.path.join(path, s)))
            source_path = os.path.join(path, files[files.__len__() - 1])
        except IndexError:
            logging.debug("Folder at '%s' is empty", path)
            raise
        else:
            return FileInfo(source_path, os.path.getmtime(source_path))

    def rotate_and_cleanup(self):
        """Cleanup backup files after sync run and rotate daily/weekly/monthly backups.
        Returns true when a new file was copied, deletions happen silently."""
        weekly_folder = os.path.join(self.folder, 'weekly')
        if not os.path.exists(weekly_folder):
            os.mkdir(weekly_folder)

        latest_file_weekly = None
        latest_file_local = None
        try:
            latest_file_weekly = self.get_latest_fileinfo(weekly_folder)
        except IndexError:
            logging.info("No weekly backups found, will use latest backup as init")

        try:
            latest_file_local = self.get_latest_fileinfo()
        except IndexError:
            logging.error("No backup files found at '%s' matching pattern '%s'",
                          self.folder, self.pattern)
            return False

        file_copied = False
        # If last file in weekly is missing or older than 7 days, move current backup
        if not latest_file_weekly or (
                latest_file_weekly.created + datetime.timedelta(days=7) < latest_file_local.created
        ):
            new_name = "%s_%s" % (datetime.datetime.now().strftime('%Y-%m-%d'),
                                  latest_file_local.name)

            target_path = os.path.join(self.folder, 'weekly', new_name)
            if not self.skip:
                shutil.copyfile(latest_file_local.path, target_path)
                file_copied = True
            else:
                logging.info(Style.DIM + "[cleanup] cp %s %s" + Style.RESET_ALL,
                             latest_file_local.path, target_path)
                file_copied = True

        # Cleanup old backups
        old_daily_backups = (bak for bak in glob.glob(os.path.join(self.folder, self.pattern))
                             if datetime.datetime.fromtimestamp(os.path.getmtime(bak)) +
                             datetime.timedelta(days=7) < datetime.datetime.now())
        for backup in old_daily_backups:
            if not self.skip:
                os.remove(backup)
            else:
                logging.info(Style.DIM + "[cleanup] rm %s" + Style.RESET_ALL, backup)

        # Cleanup old weekly backups if configured
        if self.weekly_cycle > 0:
            day_offset = self.weekly_cycle * 7
            old_weekly_backups = (bak for bak in glob.glob(os.path.join(weekly_folder, self.pattern))
                                  if datetime.datetime.fromtimestamp(os.path.getmtime(bak)) +
                                  datetime.timedelta(days=day_offset) < datetime.datetime.now())
            for backup in old_weekly_backups:
                if not self.skip:
                    os.remove(backup)
                else:
                    logging.info(Style.DIM + "[cleanup] rm %s" + Style.RESET_ALL, backup)

        return file_copied

    def do_sync(self, file):
        """Do the actual synchronization to AWS Glacier"""
        try:
            if not any(v for v in self.glacier.vaults.all() if v.name == self.vault_name):
                # Auto-create vault
                vault = self.glacier.create_vault(vaultName=self.vault_name)
        except botocore.exceptions.ClientError as cli_error:
            logging.error(cli_error.response)
            return False

        try:
            desc = "python-glacier-sync run on %s against %s%s" % (platform.node(),
                                                                   self.folder, self.pattern)
            fs_obj = open(file.path, 'rb')
            if not self.skip:
                vault = self.glacier.Vault(self.account_id, self.vault_name)
                upload_res = vault.upload_archive(archiveDescription=desc, body=fs_obj)

                # Write metadata-file with archive id
                with open(file.path + '.awsmeta.json', 'w') as metafile:
                    json.dump({
                        "archive_id": upload_res.id,
                        "account_id": upload_res.account_id,
                        "vault": upload_res.vault_name
                    }, metafile)
            else:
                logging.info(Style.DIM + "[do_sync] desc: %s" + Style.RESET_ALL, desc)
                logging.info(Style.DIM + "[do_sync] fsObject: %s" + Style.RESET_ALL, fs_obj)
        except AttributeError:
            logging.error("file object is invalid: %s", file)
            raise
        else:
            return True
