from ftw.upgrade import UpgradeStep


class UseIBlockCoordinatesBehavior(UpgradeStep):
    """Use IBlockCoordinates behavior.
    """

    def __call__(self):
        self.install_upgrade_profile()
