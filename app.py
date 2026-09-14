from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

jobs = []

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/jobs", methods=["POST"])
def add_job():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "company" not in data or "role" not in data:
        return jsonify({
            "error": "Fields 'company' and 'role' are required"
        }), 400

    if not isinstance(data["company"], str) or not data["company"].strip():
        return jsonify({"error": "Company name cannot be empty"}), 400

    if not isinstance(data["role"], str) or not data["role"].strip():
        return jsonify({"error": "Job role cannot be empty"}), 400

    job = {
        "id": len(jobs) + 1,
        "company": data["company"].strip(),
        "role": data["role"].strip(),
        "status": data.get("status", "Applied")
    }

    jobs.append(job)

    return jsonify(job), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)