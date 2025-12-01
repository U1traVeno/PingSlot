import random
import string

from sqlmodel import Session, select

from pingslot.models import Platform, User, UserBinding


class DuplicatedBindingException(Exception):
    pass


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def _generate_code(self) -> str:
        """Random six character or number invite code"""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    async def create_user(self, name: str) -> User:
        """Create a new user with a unique invite code"""
        code = await self._generate_code()
        user = User(name=name, invite_code=code)
        self.session.add(user)
        self.session.commit()
        return user

    async def bind_user(
        self, user_id: int, platform: Platform, platform_user_id: str
    ) -> UserBinding:
        """Bind a user to a platform using platform user ID"""
        # Check if binding exists
        stmt = select(UserBinding).where(
            UserBinding.platform == platform,
            UserBinding.platform_user_id == platform_user_id,
        )
        result = self.session.exec(stmt).first()
        if result:
            raise DuplicatedBindingException(
                "This platform user ID is already bound to a user."
            )

        # Create new binding
        binding = UserBinding(
            user_id=user_id, platform=platform, platform_user_id=platform_user_id
        )
        self.session.add(binding)
        self.session.commit()

        return binding
