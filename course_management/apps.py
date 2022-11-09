from django.apps import AppConfig


class CourseManagementConfig(AppConfig):
    name = 'course_management'

    def ready(self):
        import course_management.signals