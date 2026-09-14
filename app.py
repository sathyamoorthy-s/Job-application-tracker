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


@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify(jobs), 200


@app.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
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

    for job in jobs:
        if job["id"] == job_id:
            job["company"] = data["company"].strip()
            job["role"] = data["role"].strip()
            job["status"] = data.get("status", job["status"])

            return jsonify(job), 200

    return jsonify({"error": "Job application not found"}), 404


@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    for job in jobs:
        if job["id"] == job_id:
            jobs.remove(job)

            return jsonify({
                "message": "Job application deleted successfully"
            }), 200

    return jsonify({
        "error": "Job application not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)