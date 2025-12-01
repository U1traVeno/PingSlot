from sqlmodel import Session
from pingslot.models import Resource


class ResourceService:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_resource(
        self, user_id: int, name: str, description: str | None
    ) -> Resource:
        resource = Resource(user_id=user_id, name=name, description=description)
        self.session.add(resource)
        self.session.commit()
        return resource

    async def delete_resource(self, resource_id: int) -> None:
        resource = self.session.get(Resource, resource_id)
        if resource:
            self.session.delete(resource)
            self.session.commit()

    async def get_resource(self, resource_id: int) -> Resource | None:
        return self.session.get(Resource, resource_id)

    async def update_resource(
        self, resource_id: int, name: str | None, description: str | None
    ) -> Resource | None:
        resource = self.session.get(Resource, resource_id)
        if resource:
            if name is not None:
                resource.name = name
            if description is not None:
                resource.description = description
            self.session.add(resource)
            self.session.commit()
            return resource
        return None
