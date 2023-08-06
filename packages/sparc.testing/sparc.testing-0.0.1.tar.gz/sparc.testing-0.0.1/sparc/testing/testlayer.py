import sparc.testing
from zope.component.testlayer import ZCMLFileLayer
from sparc.configuration.zcml.configure import configure_vocabulary_registry

class SparcZCMLFileLayer(ZCMLFileLayer):
    def setUp(self):
        super(SparcZCMLFileLayer, self).setUp()
        configure_vocabulary_registry()
    def tearDown(self):
        super(SparcZCMLFileLayer, self).tearDown()
        

SPARC_INTEGRATION_LAYER = SparcZCMLFileLayer(sparc.testing)