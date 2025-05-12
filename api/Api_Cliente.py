from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def root():
    return "home"

@app.route("/users/<user_id>")
def get_user(user_id):
    user={"id":user_id,'name':'test','telefono':'56948486010'}
    #users/2758?query=query_test
    query= request.args.get('query')
    if query:
        user["query"]=query
    return jsonify(user),200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    data["status"] = "User created"
    return jsonify(data),201

@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    data["status"] = "User updated"
    return jsonify(data),200

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    data = request.json
    data["status"] = "User deleted"
    return jsonify(data),200





if __name__ == "__main__":
    app.run(debug = True)