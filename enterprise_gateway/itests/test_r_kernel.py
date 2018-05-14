import unittest
import re

from enterprise_gateway.itests.kernel_client import KernelLauncher


class RKernelBaseTestCase(object):
    """
    R Related test cases where there is a concrete
    test class for each available kernelspec for R kernels

    IPython related kernelspec
    - spark_R_yarn_client
    - spark_R_yarn_cluster
    """

    def test_hello_world(self):
        result = self.kernel.execute('print("Hello World", quote = FALSE)')
        assert re.search('Hello World', result)

    def test_get_application_id(self):
        result = self.kernel.execute('SparkR:::callJMethod(SparkR:::callJMethod(sc, "sc"), "applicationId")')
        assert re.search('application_', result)

    def test_get_spark_version(self):
        result = self.kernel.execute("sparkR.version()")
        assert re.search('2.1', result)

    def test_get_resource_manager(self):
        result = self.kernel.execute('unlist(sparkR.conf("spark.master"))')
        assert re.search('yarn', result)

    def test_get_deploy_mode(self):
        result = self.kernel.execute('unlist(sparkR.conf("spark.submit.deployMode"))')
        assert re.findall('(cluster|client)', result)

    def test_get_host_address(self):
        result = self.kernel.execute('unlist(sparkR.conf("spark.driver.host"))')
        assert re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result)


class TestRKernelClient(unittest.TestCase, RKernelBaseTestCase):
    GATEWAY_HOST = "localhost:8888"
    KERNELSPEC = "spark_R_yarn_client"

    @classmethod
    def setUpClass(cls):
        super(TestRKernelClient, cls).setUpClass()
        print('>>>')
        print('Starting R kernel at {} using {} kernelspec'.format(cls.GATEWAY_HOST, cls.KERNELSPEC))

        # initialize environment
        cls.launcher = KernelLauncher(cls.GATEWAY_HOST)
        cls.kernel = cls.launcher.launch(cls.KERNELSPEC)

    @classmethod
    def tearDownClass(cls):
        super(TestRKernelClient, cls).tearDownClass()
        print('Shutting down R kernel at {} using {} kernelspec'.format(cls.GATEWAY_HOST, cls.KERNELSPEC))
        # shutdown environment
        cls.launcher.shutdown(cls.kernel.kernel_id)


class TestRKernelCluster(unittest.TestCase, RKernelBaseTestCase):
    KERNELSPEC = "spark_R_yarn_cluster"

    @classmethod
    def setUpClass(cls):
        super(TestRKernelCluster, cls).setUpClass()
        print('>>>')
        print('Starting Python kernel using {} kernelspec'.format(cls.KERNELSPEC))

        # initialize environment
        cls.launcher = KernelLauncher()
        cls.kernel = cls.launcher.launch(cls.KERNELSPEC)

    @classmethod
    def tearDownClass(cls):
        super(TestRKernelCluster, cls).tearDownClass()
        print('Shutting down Python kernel using {} kernelspec'.format(cls.KERNELSPEC))
        # shutdown environment
        cls.launcher.shutdown(cls.kernel.kernel_id)


if __name__ == '__main__':
    unittest.main()