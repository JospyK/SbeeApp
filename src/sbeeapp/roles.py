from rolepermissions.roles import AbstractUserRole

class abonne(AbstractUserRole):
    available_permissions = {
        'create_medical_record': True,
    }

class admin(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }