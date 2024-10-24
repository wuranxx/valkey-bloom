import pytest, time
import os
from valkey_bloom_test_case import ValkeyBloomTestCaseBase
from valkeytests.conftest import resource_port_tracker

class TestBloomSaveRestore(ValkeyBloomTestCaseBase):

    def test_basic_save_and_restore(self):
        client = self.server.get_new_client()
        bf_add_result_1 = client.execute_command('BF.ADD testSave item')
        assert bf_add_result_1 == 1
        bf_exists_result_1 = client.execute_command('BF.EXISTS testSave item')
        assert bf_exists_result_1 == 1
        bf_info_result_1 = client.execute_command('BF.INFO testSave')
        assert(len(bf_info_result_1)) != 0
        curr_item_count_1 = client.info_obj().num_keys()
        
        # save rdb, restart sever
        client.bgsave()
        self.server.wait_for_save_done()
        # Keep the server running for 1 second more to have a larger uptime.
        time.sleep(1)
        uptime_in_sec_1 = self.client.info_obj().uptime_in_secs()
        self.server.restart(remove_rdb=False, remove_nodes_conf=False, connect_client=True)
        uptime_in_sec_2 = self.client.info_obj().uptime_in_secs()
        assert self.server.is_alive()
        assert uptime_in_sec_1 > uptime_in_sec_2
        assert self.server.is_rdb_done_loading()

        # verify restore results
        curr_item_count_2 = client.info_obj().num_keys()
        assert curr_item_count_2 == curr_item_count_1
        bf_exists_result_2 = client.execute_command('BF.EXISTS testSave item')
        assert bf_exists_result_2 == 1
        bf_info_result_2 = client.execute_command('BF.INFO testSave')
        assert bf_info_result_2 == bf_info_result_1
