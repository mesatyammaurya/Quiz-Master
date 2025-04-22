from sqlalchemy.orm import Session
from sqlalchemy import func
from models.model import *


'''================================== Function to calculate average score of the user ============================================'''
def getAvgScores(session: Session):

    avgScores = (
        session.query(User.id, func.round(func.avg(Score.totalScore), 2).label("averageScore"))
        .outerjoin(Score)  
        .group_by(User.id)
        .all()
    )

    return {userId: avg or 0.00 for userId, avg in avgScores}