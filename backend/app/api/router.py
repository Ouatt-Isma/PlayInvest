from fastapi import APIRouter
from . import users, quizzes, register, confirm_email, login, referrals, assets, graph, portfolio, investments, performance, pastperf, articles
from .Users import me 

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users", "update-password", "forgot-password", "reset-password"])
router.include_router(quizzes.router, prefix="/api", tags=["quizzes"])
router.include_router(quizzes.router, prefix="/api", tags=["/quiz-results/status"])
router.include_router(quizzes.router, prefix="/api", tags=["/quiz-results"])
router.include_router(register.router, prefix="/api", tags=["register"])
router.include_router(confirm_email.router, prefix="/api", tags=["confirm"])
router.include_router(login.router, prefix="/api", tags=["Login"])
router.include_router(me.router, prefix="/users", tags=["me"])
router.include_router(referrals.router, prefix="/api", tags=["referrals"])
router.include_router(assets.router, prefix="/api", tags=["assets", "buy"])
router.include_router(graph.router, prefix="/api", tags=["graph"])
router.include_router(portfolio.router, prefix="/api", tags=["portfolio"])
router.include_router(investments.router, prefix="/investments", tags=["history"])
router.include_router(performance.router, prefix="/api", tags=["performance"])
router.include_router(pastperf.router, prefix="/simulator", tags=["pastperf"])
router.include_router(articles.router, prefix="/api", tags=["articles"])