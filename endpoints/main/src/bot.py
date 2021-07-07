from src.preprocessing import q_bot
def getResponse(question):
    return {'message':q_bot(question)}
