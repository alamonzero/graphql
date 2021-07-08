from graphene_django import DjangoObjectType
import graphene
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "birthday"]


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=False)
        lastName = graphene.String(required=False)
        birthday = graphene.Date(required=False)

    id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, username, password, *args, **kwargs):
        user = User.objects.create(
            username=username,
            password=password,
            first_name=kwargs["firstName"] if "firstName" in kwargs else "",
            last_name=kwargs["lastName"] if "lastName" in kwargs else "",
            birthday=kwargs["birthday"] if "birthday" in kwargs else None,
        )
        return CreateUser(id=user.id)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String(required=False)
        password = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        birthday = graphene.Date(required=False)

    updated = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        User.objects.filter(pk=id).update(**kwargs)
        updated = True
        return UpdateUser(updated=updated)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
