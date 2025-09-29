from robyn import Robyn

from RobynScanIQ.controllers.document_controller import (
    get_documents,
    question_document,
    upload_document,
)

router = Robyn(__file__)


router.post('/')(upload_document)
router.post('/{doc_id}/question')(question_document)
router.get('/')(get_documents)
