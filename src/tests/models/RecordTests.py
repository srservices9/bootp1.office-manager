from bootp1.models.RecordManager import RecordService

SERVICE = RecordService()

def test_record_creation():
    # Testing creating Customer Record
    SERVICE.new_record("CUSTOMER", {"name": "Billy Lawn Service"})
