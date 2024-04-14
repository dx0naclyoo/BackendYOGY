from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.backend.services.projects import services as project_services


class AdminServices:
    async def get_letter_time_for_order(self, project_id, session: AsyncSession):
        project = await project_services.get_project_by_id(projects_id=project_id, session=session)

        deadline_data = project.deadline_date
        now_date = datetime.now(timezone.utc)

        if deadline_data > now_date:
            return True
        else:
            return False


services = AdminServices()
