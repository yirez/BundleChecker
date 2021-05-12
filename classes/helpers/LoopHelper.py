import os
import mmap
import sys


class LoopHelper:
    """
    Main Helper class containing the logic for bundle checking.

    Depending on the failed value;
    return sys.exit 1 if failed is true,
    return sys.exit 0 if failed is false
    """

    TR_POSTFIX = '_tr.'
    EN_POSTFIX = '_en.'
    BUNDLE_EXT = 'properties'
    TR_BUNDLE_EXT = TR_POSTFIX + BUNDLE_EXT
    EN_BUNDLE_EXT = EN_POSTFIX + BUNDLE_EXT
    failed = 0

    def loop_through(self, root_dir):
        """
        Control method determining the return value from the result of bundle control
        :rtype: sysexit val 0f 1 if failed, 0 if ok
        :param root_dir: the root dir to check for bundles
        """
        self.analyse_files(root_dir)
        if self.failed == 1:
            print("Bundle mismatch")
        else:
            print("Bundle check finished- No Mismatch")
        sys.exit(self.failed)

    def analyse_files(self, root_dir):
        """
        Prepares for analyses of files in work dir
        Checks for existence of TR_BUNDLE_EXT file, tries to find related EN_BUNDLE_EXT file and sends
        it to nitpick method and vice versa.

        Sets failed to 1 if any label or file is missing.

        :param root_dir: the root dir to check for bundles
        """
        for dir_path, dir_name, files in os.walk(root_dir):
            for file in files:
                complete_path = os.path.join(dir_path, file)
                try:
                    if file.endswith(self.TR_BUNDLE_EXT):
                        tr_file_path = ""
                        en_file_path = complete_path.replace(self.TR_POSTFIX, self.EN_POSTFIX)
                        self.nitpick(complete_path, en_file_path, self.EN_POSTFIX)  # check for missing tr items in en

                    if file.endswith(self.EN_BUNDLE_EXT):
                        en_file_path = ""
                        tr_file_path = complete_path.replace(self.EN_POSTFIX, self.TR_POSTFIX)
                        self.nitpick(complete_path, tr_file_path, self.TR_POSTFIX)  # check for missing en items in tr
                except Exception as generic:
                    self.failed = 1
                    print(generic)
                    print('Related files:\n' + (en_file_path or complete_path)
                          + '\n' + (tr_file_path or complete_path) + '\n')

    def nitpick(self, source_file, target_file, target_postfix):
        """
        Tries to find labels in source file in target file
        :param source_file:
        :param target_file:
        :param target_postfix: The target postfix to easily find missing label harboring files
        """
        with open(source_file) as file, open(target_file) as file_en:
            mmap_en_file = mmap.mmap(file_en.fileno(), 0, access=mmap.ACCESS_READ)  # get mmap for en file
            for bundle_line in file:  # bundle lines in source file
                if bundle_line.find('=') >= 0:
                    bundle_key = bundle_line[0:bundle_line.find('=')].strip()  # get bundle key

                    if mmap_en_file.find(bundle_key.encode()) == -1:
                        # if not able to find line in target file, set as failed
                        print('Key-val pair -> ' + os.path.basename(
                            source_file) + ' : ' + bundle_key + ' not found in ' + target_postfix)
                        self.failed = 1
