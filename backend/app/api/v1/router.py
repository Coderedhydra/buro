from fastapi import APIRouter
from .routes.health import router as health_router
from .routes.scan import router as scan_router
from .routes.inventory import router as inventory_router
from .routes.endpoint import router as endpoint_router
from .routes.probe import router as probe_router
from .routes.findings import router as findings_router
from .routes.report import router as report_router
from .routes.approvals import router as approvals_router
from .routes.config import router as config_router
from .routes.planner import router as planner_router
from .routes.analyzer import router as analyzer_router
from .routes.oneclick import router as oneclick_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(config_router, prefix="/config", tags=["config"])
api_router.include_router(oneclick_router, prefix="/oneclick", tags=["oneclick"])
api_router.include_router(planner_router, prefix="/planner", tags=["planner"])
api_router.include_router(analyzer_router, prefix="/analyzer", tags=["analyzer"])
api_router.include_router(scan_router, prefix="/scan", tags=["scan"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
api_router.include_router(endpoint_router, prefix="/endpoint", tags=["endpoint"])
api_router.include_router(probe_router, prefix="/probe", tags=["probe"])
api_router.include_router(findings_router, prefix="/findings", tags=["findings"])
api_router.include_router(report_router, prefix="/report", tags=["report"])
api_router.include_router(approvals_router, prefix="/findings", tags=["approvals"])