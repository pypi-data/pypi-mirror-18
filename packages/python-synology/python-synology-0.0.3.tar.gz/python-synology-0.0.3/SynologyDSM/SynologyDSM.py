"""Module containing multiple classes to interact with Synology DSM"""
# -*- coding:utf-8 -*-
import requests
from requests.compat import json


class SynoFormatHelper(object):
    """Class containing various formatting functions"""
    @staticmethod
    def bytes_to_readable(num):
        """Converts bytes to a human readable format"""
        if num < 512:
            return "0 Kb"
        elif num < 1024:
            return "1 Kb"

        for unit in ['', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb']:
            if abs(num) < 1024.0:
                return "%3.1f%s" % (num, unit)
            num /= 1024.0
        return "%.1f%s" % (num, 'Yb')


class SynoUtilization(object):
    """Class containing Utilisation data"""
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)

    def update(self, raw_input):
        """Allows updating Utilisation data with raw_input data"""
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def cpu_other_load(self):
        """'Other' percentage of the total cpu load"""
        if self._data is not None:
            return self._data["cpu"]["other_load"]

    @property
    def cpu_user_load(self):
        """'User' percentage of the total cpu load"""
        if self._data is not None:
            return self._data["cpu"]["user_load"]

    @property
    def cpu_system_load(self):
        """'System' percentage of the total cpu load"""
        if self._data is not None:
            return self._data["cpu"]["system_load"]

    @property
    def cpu_total_load(self):
        """Total CPU load for Synology DSM"""
        return self.cpu_system_load + self.cpu_user_load + self.cpu_other_load

    @property
    def cpu_1min_load(self):
        """Average CPU load past minute"""
        if self._data is not None:
            return self._data["cpu"]["1min_load"]

    @property
    def cpu_5min_load(self):
        """Average CPU load past 5 minutes"""
        if self._data is not None:
            return self._data["cpu"]["5min_load"]

    @property
    def cpu_15min_load(self):
        """Average CPU load past 15 minutes"""
        if self._data is not None:
            return self._data["cpu"]["15min_load"]

    @property
    def memory_real_usage(self):
        """Real Memory Usage from Synology DSM"""
        if self._data is not None:
            return str(self._data["memory"]["real_usage"])

    @property
    def memory_size(self):
        """Total Memory Size of Synology DSM"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["memory_size"]) * 1024)

    @property
    def memory_available_swap(self):
        """Total Available Memory Swap"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["avail_swap"]) * 1024)

    @property
    def memory_cached(self):
        """Total Cached Memory"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["cached"]) * 1024)

    @property
    def memory_available_real(self):
        """Real available memory"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["avail_real"]) * 1024)

    @property
    def memory_total_real(self):
        """Total available real memory"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["total_real"]) * 1024)

    @property
    def memory_total_swap(self):
        """Total Swap Memory"""
        if self._data is not None:
            # Memory is actually returned in KB's so multiply before converting
            return SynoFormatHelper.bytes_to_readable(
                int(self._data["memory"]["total_swap"]) * 1024)

    def _get_network(self, network_id):
        """Function to get specific network (eth0, total, etc)"""
        if self._data is not None:
            for network in self._data["network"]:
                if network["device"] == network_id:
                    return network

    @property
    def network_up(self):
        """Total upload speed being used"""
        network = self._get_network("total")
        if network is not None:
            return SynoFormatHelper.bytes_to_readable(
                int(network["tx"]))

    @property
    def network_down(self):
        """Total download speed being used"""
        network = self._get_network("total")
        if network is not None:
            return SynoFormatHelper.bytes_to_readable(
                int(network["rx"]))


class SynoStorage(object):
    """Class containing Storage data"""
    def __init__(self, raw_input):
        self._data = None
        self.update(raw_input)

    def update(self, raw_input):
        """Allows updating Utilisation data with raw_input data"""
        if raw_input is not None:
            self._data = raw_input["data"]

    @property
    def volumes(self):
        """Returns all available volumes"""
        if self._data is not None:
            volumes = []
            for volume in self._data["volumes"]:
                volumes.append(volume["id"])
            return volumes

    def _get_volume(self, volume_id):
        """Returns a specific volume"""
        if self._data is not None:
            for volume in self._data["volumes"]:
                if volume["id"] == volume_id:
                    return volume

    def volume_status(self, volume):
        """Status of the volume (normal, degraded, etc)"""
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["status"]

    def volume_device_type(self, volume):
        """Returns the volume type (RAID1, RAID2, etc)"""
        volume = self._get_volume(volume)
        if volume is not None:
            return volume["device_type"]

    def volume_size_total(self, volume):
        """Total size of volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            return SynoFormatHelper.bytes_to_readable(
                int(volume["size"]["total"]))

    def volume_size_used(self, volume):
        """Total used size in volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            return SynoFormatHelper.bytes_to_readable(
                int(volume["size"]["used"]))

    def volume_disk_temp_avg(self, volume):
        """Average temperature of all disks making up the volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            vol_disks = volume["disks"]
            if vol_disks is not None:
                total_temp = 0
                total_disks = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp is not None:
                        total_disks += 1
                        total_temp += disk_temp

                if total_temp > 0 and total_disks > 0:
                    return round(total_temp / total_disks, 0)

    def volume_disk_temp_max(self, volume):
        """Maximum temperature of all disks making up the volume"""
        volume = self._get_volume(volume)
        if volume is not None:
            vol_disks = volume["disks"]
            if vol_disks is not None:
                max_temp = 0

                for vol_disk in vol_disks:
                    disk_temp = self.disk_temp(vol_disk)
                    if disk_temp is not None and disk_temp > max_temp:
                        max_temp = disk_temp

                return max_temp

    @property
    def disks(self):
        """Returns all available (internal) disks"""
        if self._data is not None:
            disks = []
            for disk in self._data["disks"]:
                disks.append(disk["id"])
            return disks

    def _get_disk(self, disk_id):
        """Returns a specific disk"""
        if self._data is not None:
            for disk in self._data["disks"]:
                if disk["id"] == disk_id:
                    return disk

    def disk_name(self, disk):
        """The name of this disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["name"]

    def disk_device(self, disk):
        """The mount point of this disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["device"]

    def disk_smart_status(self, disk):
        """Status of disk according to S.M.A.R.T)"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["smart_status"]

    def disk_status(self, disk):
        """Status of disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["status"]

    def disk_exceed_bad_sector_thr(self, disk):
        """Checks if disk has exceeded maximum bad sector threshold"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["exceed_bad_sector_thr"]

    def disk_below_remain_life_thr(self, disk):
        """Checks if disk has fallen below minimum life threshold"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["below_remain_life_thr"]

    def disk_temp(self, disk):
        """Returns the temperature of the disk"""
        disk = self._get_disk(disk)
        if disk is not None:
            return disk["temp"]


class SynologyDSM():
    """Class containing the main Synology DSM functions"""
    def __init__(self, dsm_ip, port, username, password):
        # Store Variables
        self.username = username
        self.password = password

        # Class Variables
        self.access_token = None
        self._utilisation = None
        self._storage = None

        # Build Variables
        self.base_url = "http://%s:%s/webapi" % (dsm_ip, port)

        # Login to get our access token
        self._login()

    def _login(self):
        """Build and execute login request"""
        api_path = "%s/auth.cgi?api=SYNO.API.Auth&version=2" % (
            self.base_url,
        )
        login_path = "method=login&account=%s&passwd=%s" % (
            self.username,
            self.password
        )
        url = "%s&%s&session=Core&format=cookie" % (
            api_path,
            login_path)
        result = self._get_url(url)

        # Parse Result if valid
        if result is not None:
            self.access_token = result["data"]["sid"]

    def _get_url(self, url, retry_on_error=True):
        """Function to execute and handle a GET request"""
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                json_data = json.loads(resp.text)
                if json_data["success"]:
                    return json_data
                else:
                    if retry_on_error:
                        return self._get_url(url, False)
                    else:
                        return None
        except:
            return None

    def update(self):
        """Updates the various instanced modules"""
        if self._utilisation is not None:
            api = "SYNO.Core.System.Utilization"
            url = "%s/entry.cgi?api=%s&version=1&method=get&_sid=%s" % (
                self.base_url,
                api,
                self.access_token)
            self._utilisation.update(self._get_url(url))
        if self._storage is not None:
            api = "SYNO.Storage.CGI.Storage"
            url = "%s/entry.cgi?api=%s&version=1&method=load_info&_sid=%s" % (
                self.base_url,
                api,
                self.access_token)
            self._storage.update(self._get_url(url))

    @property
    def utilisation(self):
        """Getter for various Utilisation variables"""
        if self._utilisation is None:
            api = "SYNO.Core.System.Utilization"
            url = "%s/entry.cgi?api=%s&version=1&method=get&_sid=%s" % (
                self.base_url,
                api,
                self.access_token)
            self._utilisation = SynoUtilization(self._get_url(url))
        return self._utilisation

    @property
    def storage(self):
        """Getter for various Storage variables"""
        if self._storage is None:
            api = "SYNO.Storage.CGI.Storage"
            url = "%s/entry.cgi?api=%s&version=1&method=load_info&_sid=%s" % (
                self.base_url,
                api,
                self.access_token)
            self._storage = SynoStorage(self._get_url(url))
        return self._storage
