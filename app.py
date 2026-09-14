from flask import Flask, request, jsonify

app = Flask(__name__)

jobs = []


@app.route("/jobs", methods=["POST"])
def add_job():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "company" not in data or "role" not in data:
        return jsonify({
            "error": "Fields 'company' and 'role' are required"
        }), 400

    job = {
        "id": len(jobs) + 1,
        "company": data["company"],
        "role": data["role"],
        "status": data.get("status", "Applied")
    }

    jobs.append(job)

    return jsonify(job), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)