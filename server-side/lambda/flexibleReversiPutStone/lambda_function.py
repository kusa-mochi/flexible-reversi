import boto3
from decimal import Decimal
import json

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table('flexible-reversi-tokens')
appData = dynamodb.Table('flexible-reversi')

def rooms_default_dumps(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def between(n, min, max):
    return (min <= n and n <= max)

# board [Array<Array<number>>]: current board status. 0=empty, 1=black, 2=white, 3=wall
# iColumn [number]: column position to put stone.
# iRow [number]: row position to put stone.
# playerColor [number]: stone color to put. 1=black, 2=white
# dirColumn: -1=left, 0=no move, 1=right
# dirRow: -1=up, 0=no move, 1=down
def canPutOnDirection(board, iColumn, iRow, playerColor, dirColumn, dirRow):
    if board[iRow][iColumn] != 0:
        return False
    
    xNeighbor = iColumn + dirColumn
    yNeighbor = iRow + dirRow
    boardWidth = len(board[0])
    boardHeight = len(board)
    if between(xNeighbor, 0, boardWidth - 1) == False or between(yNeighbor, 0, boardHeight - 1) == False:
        return False
    
    x = xNeighbor
    y = yNeighbor
    opponentPlayerColor = 1 if playerColor == 2 else 2
    
    if board[y][x] != opponentPlayerColor:
        return False
    
    x += dirColumn
    y += dirRow
    while between(x, 0, boardWidth - 1) == True and between(y, 0, boardHeight - 1) == True:
        if board[y][x] == playerColor:
            return True
        if board[y][x] == opponentPlayerColor:
            x += dirColumn
            y += dirRow
        else:
            return False
    
    return False

# board [Array<Array<number>>]: current board status. 0=empty, 1=black, 2=white, 3=wall
# iColumn [number]: column position to put stone.
# iRow [number]: row position to put stone.
# playerColor [number]: stone color to put. 1=black, 2=white
def canPutStone(board, iColumn, iRow, playerColor):
    up        = canPutOnDirection(board, iColumn, iRow, playerColor,  0, -1)
    upRight   = canPutOnDirection(board, iColumn, iRow, playerColor,  1, -1)
    right     = canPutOnDirection(board, iColumn, iRow, playerColor,  1,  0)
    downRight = canPutOnDirection(board, iColumn, iRow, playerColor,  1,  1)
    down      = canPutOnDirection(board, iColumn, iRow, playerColor,  0,  1)
    downLeft  = canPutOnDirection(board, iColumn, iRow, playerColor, -1,  1)
    left      = canPutOnDirection(board, iColumn, iRow, playerColor, -1,  0)
    upLeft    = canPutOnDirection(board, iColumn, iRow, playerColor, -1, -1)
    
    if up or upRight or right or downRight or down or downLeft or left or upLeft:
        return True
    else:
        return False

def canPutStoneOnAnywhere(board, playerColor):
    boardWidth = len(board[0])
    boardHeight = len(board)
    for iRow in range(boardHeight):
        for iColumn in range(boardWidth):
            if canPutStone(board, iColumn, iRow, playerColor) == True:
                return True
    return False

# board [Array<Array<number>>]: current board status. 0=empty, 1=black, 2=white, 3=wall
# iColumn [number]: column position to put stone.
# iRow [number]: row position to put stone.
# playerColor [number]: stone color to put. 1=black, 2=white
# dirColumn: -1=left, 0=no move, 1=right
# dirRow: -1=up, 0=no move, 1=down
def putStoneOnDirection(board, iColumn, iRow, playerColor, dirColumn, dirRow):
    xNeighbor = iColumn + dirColumn
    yNeighbor = iRow + dirRow
    boardWidth = len(board[0])
    boardHeight = len(board)
    if between(xNeighbor, 0, boardWidth - 1) == False or between(yNeighbor, 0, boardHeight - 1) == False:
        return
    
    x = xNeighbor
    y = yNeighbor
    opponentPlayerColor = 1 if playerColor == 2 else 2
    
    if board[y][x] != Decimal(opponentPlayerColor):
        return
    
    x += dirColumn
    y += dirRow
    while between(x, 0, boardWidth - 1) == True and between(y, 0, boardHeight - 1) == True:
        if board[y][x] == Decimal(playerColor):
            board[iRow][iColumn] = Decimal(playerColor)
            m = xNeighbor
            n = yNeighbor
            while board[n][m] == Decimal(opponentPlayerColor):
                print('row:')
                print(n)
                print('column:')
                print(m)
                print('color:')
                print(playerColor)
                board[n][m] = Decimal(playerColor)
                m += dirColumn
                n += dirRow
            break
        if board[y][x] == Decimal(opponentPlayerColor):
            x += dirColumn
            y += dirRow
        else:
            return
    return

# board [Array<Array<number>>]: current board status. 0=empty, 1=black, 2=white, 3=wall
# iColumn [number]: column position to put stone.
# iRow [number]: row position to put stone.
# playerColor [number]: stone color to put. 1=black, 2=white
def putStone(board, iColumn, iRow, playerColor):
    if board[iRow][iColumn] != Decimal(0):
        return
    putStoneOnDirection(board, iColumn, iRow, playerColor,  0, -1)
    putStoneOnDirection(board, iColumn, iRow, playerColor,  1, -1)
    putStoneOnDirection(board, iColumn, iRow, playerColor,  1,  0)
    putStoneOnDirection(board, iColumn, iRow, playerColor,  1,  1)
    putStoneOnDirection(board, iColumn, iRow, playerColor,  0,  1)
    putStoneOnDirection(board, iColumn, iRow, playerColor, -1,  1)
    putStoneOnDirection(board, iColumn, iRow, playerColor, -1,  0)
    putStoneOnDirection(board, iColumn, iRow, playerColor, -1, -1)
    return

def countBoardElement(board, element):
    ret = 0
    for row in board:
        ret += row.count(element)
    return ret

def hasEmptyCell(board):
    return countBoardElement(board, 0) > 0

def lambda_handler(event, context):
    print("putStone start.")
    print(event)
    
    # check a token from a client.
    postData = json.loads(event.get('body', '{}')).get('data')
    token = postData['token']
    print(postData)
    connection = connections.get_item(Key={'token': token})
    print(connection)
    # if a token is not exist on DB
    if token != connection['Item']['token']:
        return {
            'statusCode': 404,
            'body': json.dumps('access denied.')
        }
    
    # current player token
    currentPlayerToken = token
    
    # room id
    roomId = postData['roomId']
    print('room id:')
    print(roomId)
    
    # column
    iColumn = postData['column']
    print('iColumn')
    print(iColumn)
    
    # row
    iRow = postData['row']
    print('iRow')
    print(iRow)
    
    # room data
    roomData = appData.get_item(Key={'id': roomId})['Item']
    
    # current player: True=room author, False=opponent
    currentPlayer = True
    
    # first (black) player: True=room author, False=opponent
    firstPlayer = roomData['firstPlayer']
    
    # current player color: 1=black, 2=white, -1=NULL
    currentPlayerColor = -1
    if roomData['roomAuthorId'] == currentPlayerToken:
        currentPlayer = True
        # if first player(black) is room author
        if firstPlayer == True:
            # current player color is black
            currentPlayerColor = 1
        else:
            # current player color is white
            currentPlayerColor = 2
    elif roomData['opponentId'] == currentPlayerToken:
        currentPlayer = False
        # if first player(black) is room author
        if firstPlayer == True:
            # current player color is white
            currentPlayerColor = 2
        else:
            # current player color is black
            currentPlayerColor = 1
    else:
        raise ValueError('a value of currentPlayerColor cannot be defined.')

    # get current board status from DB.
    currentBoardStatus = roomData['currentBoard']

    # check if it can put stone on the specified position (column, row).
    canPut = canPutStone(currentBoardStatus, iColumn, iRow, currentPlayerColor)
    
    if canPut == True:
        print('can put!')
        print('before putting:')
        print(currentBoardStatus)
        putStone(currentBoardStatus, iColumn, iRow, currentPlayerColor)
        print('after putting:')
        print(currentBoardStatus)
    else:
        print('cannot put')
    
    nextPlayerColor = 1 if currentPlayerColor == 2 else 2
    
    # return raw values
    retToRoomAuthor = {
        'dataType': 'putStone',
        'data': {
            'boardStatus': [],
            'nextPlayer': '',  # 'you'/'notYou'
            'black': 0,
            'white': 0,
            'empty': 0
        }
    }
    retToOpponent = {
        'dataType': 'putStone',
        'data': {
            'boardStatus': [],
            'nextPlayer': '',
            'black': 0,
            'white': 0,
            'empty': 0
        }
    }
    
    # count board elements
    retToRoomAuthor['data']['black'] = countBoardElement(currentBoardStatus, 1)
    retToRoomAuthor['data']['white'] = countBoardElement(currentBoardStatus, 2)
    retToRoomAuthor['data']['empty'] = countBoardElement(currentBoardStatus, 0)
    retToOpponent['data']['black'] = retToRoomAuthor['data']['black']
    retToOpponent['data']['white'] = retToRoomAuthor['data']['white']
    retToOpponent['data']['empty'] = retToRoomAuthor['data']['empty']
    
    retToRoomAuthor['data']['boardStatus'] = currentBoardStatus
    retToOpponent['data']['boardStatus'] = currentBoardStatus
    
    # if a room author is black
    if firstPlayer == True:
        numRoomAuthorStones = countBoardElement(currentBoardStatus, 1)
        numOpponentStones = countBoardElement(currentBoardStatus, 2)
    else:
        numRoomAuthorStones = countBoardElement(currentBoardStatus, 2)
        numOpponentStones = countBoardElement(currentBoardStatus, 1)
    
    # if there is no empty cell
    if hasEmptyCell(currentBoardStatus) == False:
        print('hasEmptyCell(currentBoardStatus) == False')
        # game is set.
        if numRoomAuthorStones > numOpponentStones:
            retToRoomAuthor['data']['nextPlayer'] = 'youWin'
            retToOpponent['data']['nextPlayer'] = 'youLose'
        elif numRoomAuthorStones == numOpponentStones:
            retToRoomAuthor['data']['nextPlayer'] = 'draw'
            retToOpponent['data']['nextPlayer'] = 'draw'
        else:
            retToRoomAuthor['data']['nextPlayer'] = 'youLose'
            retToOpponent['data']['nextPlayer'] = 'youWin'
    else:
        print('hasEmptyCell(currentBoardStatus) != False')
        # if next player cannot put its stone
        if canPutStoneOnAnywhere(currentBoardStatus, nextPlayerColor) == False:
            print('canPutStoneOnAnywhere(currentBoardStatus, nextPlayerColor) == False')
            # if current player also cannot put its stone
            if canPutStoneOnAnywhere(currentBoardStatus, currentPlayerColor) == False:
                print('canPutStoneOnAnywhere(currentBoardStatus, currentPlayerColor) == False')
                # game is set.
                if numRoomAuthorStones > numOpponentStones:
                    retToRoomAuthor['data']['nextPlayer'] = 'youWin'
                    retToOpponent['data']['nextPlayer'] = 'youLose'
                elif numRoomAuthorStones == numOpponentStones:
                    retToRoomAuthor['data']['nextPlayer'] = 'draw'
                    retToOpponent['data']['nextPlayer'] = 'draw'
                else:
                    retToRoomAuthor['data']['nextPlayer'] = 'youLose'
                    retToOpponent['data']['nextPlayer'] = 'youWin'
            else:
                print('canPutStoneOnAnywhere(currentBoardStatus, currentPlayerColor) != False')
                # next player is current player again.
                if currentPlayer == True:
                    print('currentPlayer == True')
                    retToRoomAuthor['data']['nextPlayer'] = 'you'
                    retToOpponent['data']['nextPlayer'] = 'notYou'
                else:
                    print('currentPlayer != True')
                    retToRoomAuthor['data']['nextPlayer'] = 'notYou'
                    retToOpponent['data']['nextPlayer'] = 'you'
        else:
            print('canPutStoneOnAnywhere(currentBoardStatus, nextPlayerColor) != False')
            # change player.
            if currentPlayer == True:
                print('currentPlayer == True')
                retToRoomAuthor['data']['nextPlayer'] = 'notYou'
                retToOpponent['data']['nextPlayer'] = 'you'
            else:
                print('currentPlayer != True')
                retToRoomAuthor['data']['nextPlayer'] = 'you'
                retToOpponent['data']['nextPlayer'] = 'notYou'
    
    # return values
    jsonToRoomAuthor = json.dumps(retToRoomAuthor, default=rooms_default_dumps)
    jsonToOpponent = json.dumps(retToOpponent, default=rooms_default_dumps)
    
    # room author token
    roomAuthorToken = roomData['roomAuthorId']
    # opponent token
    opponentToken = roomData['opponentId']
    
    # room author connection
    roomAuthorConnection = connections.get_item(Key={'token': roomAuthorToken})
    # opponent connection
    opponentConnection = connections.get_item(Key={'token': opponentToken})
    
    # room author endpoint url
    roomAuthorUrl = roomAuthorConnection['Item']['endpointUrl']
    # opponent endpoint url
    opponentUrl = opponentConnection['Item']['endpointUrl']
    
    # room author connection id
    roomAuthorConnectionId = roomAuthorConnection['Item']['connectionId']
    # opponent connection id
    opponentConnectionId = opponentConnection['Item']['connectionId']
    
    # send data to players.
    am = boto3.client('apigatewaymanagementapi', endpoint_url=roomAuthorUrl)
    _ = am.post_to_connection(ConnectionId=roomAuthorConnectionId, Data=jsonToRoomAuthor)
    am = boto3.client('apigatewaymanagementapi', endpoint_url=opponentUrl)
    _ = am.post_to_connection(ConnectionId=opponentConnectionId, Data=jsonToOpponent)
    
    # update room data
    
    # if game is set
    if retToRoomAuthor['data']['nextPlayer'] == 'youWin' or retToRoomAuthor['data']['nextPlayer'] == 'youLose':
        print('game is set.')
        sendData = "{\"data\":{\"token\":\"" + roomAuthorToken + "\","
        sendData += "\"id\":" + str(roomId) + ","
        sendData += "\"boardLogs\":[],"
        sendData += "\"canView\":false,"
        sendData += "\"currentBoard\":[],"
        sendData += "\"currentPlayer\":true,"
        sendData += "\"entryPassword\":\"\","
        sendData += "\"firstPlayer\":true,"
        sendData += "\"requireEntryPassword\":false,"
        sendData += "\"roomName\":\"\","
        sendData += "\"roomState\":\"vacancy\","
        sendData += "\"thinkingCounter\":0,"
        sendData += "\"opponentId\":\"4dc4a59af1a341ee468607550985aa4a23437d5061c365f341aad92b09176035\","
        sendData += "\"opponentName\":\"\","
        sendData += "\"roomAuthorId\":\"4dc4a59af1a341ee468607550985aa4a23437d5061c365f341aad92b09176035\","
        sendData += "\"roomAuthor\":\"\""
        sendData += "}}"
        response = boto3.client('lambda').invoke(
            FunctionName='arn:aws:lambda:ap-northeast-1:280196608156:function:flexibleReversiUpdateRoom',
            InvocationType='Event',
            Payload=json.dumps({'body':sendData, 'requestContext':{'connectionId':roomAuthorConnectionId}})
        )
        return {
            'statusCode': 200,
            'body': json.dumps('gameSet')
        }
    
    exp = 'set currentBoard=:currentBoard,currentPlayer=:currentPlayer'
    eav = {
        ':currentBoard': currentBoardStatus,
        ':currentPlayer': retToRoomAuthor['data']['nextPlayer'] == 'you'
    }

    # if currentPlayer == True:
    #     exp += ',roomAuthor=:roomAuthor'
    #     eav[':roomAuthor'] = postData['nickname']
    # else:
    #     exp += ',opponentName=:opponentName'
    #     eav[':opponentName'] = postData['nickname']
    result = appData.update_item(
        Key={'id': roomId},
        UpdateExpression=exp,
        ExpressionAttributeValues=eav,
        ReturnValues='UPDATED_NEW'
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('putStone')
    }
