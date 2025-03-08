import json, os

def createprompt(body:json):
    user_data = body.get("new_member", {})

    file_path = os.path.abspath(os.path.join(
                                    os.path.dirname(
                                            os.path.realpath(__file__)
                                            )
                                                , '..', 'tamplates', 'prompt.txt'
                                        )
                                )

    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()




    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({"prompt": prompt}),
    #     "headers": {
    #         "Content-Type": "application/json"
    #     }
    # }
