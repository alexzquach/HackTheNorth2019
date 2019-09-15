# THE MAIN GAME
# WRITTEN BY RYAN, ALEX, ZUHAB AND VERONICA
from ChessLib import *
from parsing import *
import chess.svg
import azure.cognitiveservices.speech as speechsdk

if __name__ == '__main__':
    board = chess.Board()
    #output_board(str(board))
    # Continuing looping while the game is not over
    while not board.is_game_over():
        playerCommand = 0
        # Determine whose turn it is
        if(board.turn):
            print("Its White's Turn, ")
        else:
            print("Its Black's Turn, ")

        # ###### TAKE IN A VOICE COMMAND ######

        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        speech_key, service_region = "243894c653d944869a8ab5f28f9f60bf", "canadacentral"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

        print("Say a valid move...")

        # Starts speech recognition, and returns after a single utterance is recognized. The end of a
        # single utterance is determined by listening for silence at the end or until a maximum of 15
        # seconds of audio is processed.  The task returns the recognition text as result.
        # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
        # shot recognition like command or query.
        # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
        result = speech_recognizer.recognize_once()
        print("processing move...")
        # Checks result.
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Speech Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        ###### PARSE THE VOICE COMMAND INTO A MOVE ######
        speech_input = str(result.text)

        ###### MAKE THE MOVE, PUSH THE NEW BOARD ######
        move = parse_move(speech_input)[0]

        # End the game
        if move == 'end':
            print("Are you sure?")
            result = speech_recognizer.recognize_once()
            # Confirm the game ending
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Speech Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            if str(result.text).strip().lower().strip().replace('.', '') == "yes" or str(
                    result.text).strip().lower().strip().replace('.', '') \
                    == "yeah" or str(result.text).strip().lower().strip().replace('.', '') == "sure":
                print("Game over! Force end.")
                break
            playerCommand = 1

        # Forfeitting
        if move == 'forfeit':
            print("Are you sure?")
            result = speech_recognizer.recognize_once()
            # Checks result.
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Speech Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            if str(result.text).strip().lower().strip().replace('.', '') == "yes" or str(result.text).strip().lower().strip().replace('.', '')\
                    == "yeah" or str(result.text).strip().lower().strip().replace('.', '') == "sure":
                print("Game over! Forfeitted by user.")
                break
            playerCommand = 1

        # Check draw status
        if move == 'draw':

            counter = 0
            print("Player White, are you sure?")
            result = speech_recognizer.recognize_once()
            # Checks result.
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Speech Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            # If player white said yes to draw, ask player black as well
            if str(result.text).strip().lower().strip().replace('.', '') == "yes" or str(
                    result.text).strip().lower().strip().replace('.', '') \
                    == "yeah" or str(result.text).strip().lower().strip().replace('.', '') == "sure":
                counter += 1
                # Only ask player black if player white wants a draw as well
                print("Player Black, are you sure?")
                result = speech_recognizer.recognize_once()
                # Checks result.
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    print("Speech Recognized: {}".format(result.text))
                elif result.reason == speechsdk.ResultReason.NoMatch:
                    print("No speech could be recognized: {}".format(result.no_match_details))
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print("Error details: {}".format(cancellation_details.error_details))
                if str(result.text).strip().lower().strip().replace('.', '') == "yes" or str(
                        result.text).strip().lower().strip().replace('.', '') \
                        == "yeah" or str(result.text).strip().lower().strip().replace('.', '') == "sure":
                    counter += 1
            # If both players agree, draw the game
            if counter == 2:
                print("Game over! Game draw.")
                break
            playerCommand = 1

        if move.lower()=="redo":
            try:
                board.pop()
            except:
                print("Nothing to undo!")
            #output_board(str(board))
        else:
            try:
                board.push_san(move)
                #output_board(str(board))
            except:
                if playerCommand == 0:
                    print("Invalid move, please try again!")
            # Write our board
            boardFile = open("board.svg","w")
            svg = chess.svg.board(board=board,squares=None,coordinates=True)
            strsvg = str(svg)
            boardFile.write(strsvg)
            boardFile.close()
