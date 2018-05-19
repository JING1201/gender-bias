from genderbias.effort import EffortDetector
from genderbias.document import Document

BAD_DOCUMENTS = [
    """NAME always tried her best, was patient, and had great insight.""",
    """Everyone knows that NAME is persistent.""",
]

GOOD_DOCUMENTS = [
    """NAME was professional and innovative.""",
    """NAME consistently delivered results.""",
]


def test_bad_documents_trip_detector():
    for doc in BAD_DOCUMENTS:
        [
            print(f) for f in EffortDetector().get_flags(Document(doc))
        ]
        assert(
            len(EffortDetector().get_flags(Document(doc))) > 0
        )


def test_good_documents_pass_detector():
    for doc in GOOD_DOCUMENTS:
        assert(
            len(EffortDetector().get_flags(Document(doc))) == 0
        )
