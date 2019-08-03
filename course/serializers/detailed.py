from user_profile.serializer import UserSerializer
from adplatform.serializers.tag import TagSerializer
from course.serializers import listing


class AssignmentSerializer(listing.AssignmentSerializer):
    author = UserSerializer(many=False, read_only=True)


class LessonSerializer(listing.LessonSerializer):
    author = UserSerializer(many=False, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)


class ModuleSerializer(listing.ModuleSerializer):
    author = UserSerializer(many=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)


class CourseSerializer(listing.CourseSerializer):
    """
    For detailed course information
    """
    author = UserSerializer(many=False, read_only=True)
    tagged_to = TagSerializer(many=True, read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
