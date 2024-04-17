from flask import Flask, request, abort, jsonify
from models import setup_db, Student, Instructor
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/allStudents', methods=['GET'])
    @requires_auth('get:students')
    def allStudents():
        try:
            students = Student.query.all()
            formatted_students = [student.format() for student in students]
            if formatted_students == []:
                abort(404)
            return jsonify({
                'success': True,
                'students': formatted_students,
                'totalStudents': len(students)
                })
        except Exception:
            abort(404)

    @app.route('/student', methods=['POST'])
    @requires_auth('post: student')
    def addStudent():
        content = request.get_json()
        new_name = content.get('name', None)
        if new_name is None:
            abort(400)
        new_studyLanguage = content.get('studyLanguage', None)
        if new_studyLanguage is None:
            abort(400)
        new_nativeLanguage = content.get('nativeLanguage', None)
        if new_nativeLanguage is None:
            abort(400)
        try:
            student = Student(
                      name=new_name,
                      studyLanguage=new_studyLanguage,
                      nativeLanguage=new_nativeLanguage)
            student.insert()
            students = Student.query.all()
            return jsonify({
                'success': True,
                'created': student.id,
                'totalStudents': len(students)
                })
        except Exception:
            abort(400)

    @app.route('/student/<int:student_id>', methods=['PATCH'])
    @requires_auth('patch: student')
    def updateStudent(student_id):
        student = Student.query.filter(Student.id == student_id).one_or_none()
        if student is None:
            abort(404)
        content = request.get_json()
        student.name = content.get('name', None)
        student.studyLanguage = content.get('studyLanguage', None)
        student.nativeLanguage = content.get('nativeLanguage', None)
        student.update()
        return jsonify({
            "success": True,
            "name":  student.name,
            "studyLanguage": student.studyLanguage,
            "nativeLanguage": student.nativeLanguage
            })

    @app.route('/student/<int:student_id>', methods=['DELETE'])
    @requires_auth('delete: student')
    def deleteStudent(student_id):
        try:
            student = Student.query.filter(
                      Student.id == student_id).one_or_none()
            if student is None:
                abort(404)
            student.delete()
            students = Student.query.all()
            return jsonify({
                'success': True,
                'totalstudents': len(students)
                })
        except Exception:
            abort(404)

    @app.route('/allInstructors', methods=['GET'])
    @requires_auth('get: instructors')
    def allInstructors():
        try:
            instructors = Instructor.query.all()
            formatted_instructors = [
                instructor.format() for instructor in instructors]
            if formatted_instructors == []:
                abort(404)
            return jsonify({
                'success': True,
                'instructors': formatted_instructors,
                'totalInstructors': len(instructors)
                })
        except Exception:
            abort(404)

    @app.route('/instructor', methods=['POST'])
    @requires_auth('post: instructor')
    def addInstructor():
        content = request.get_json()
        new_name = content.get('name', None)
        if new_name is None:
            abort(400)
        new_teachLanguage = content.get('teachLanguage', None)
        if new_teachLanguage is None:
            abort(400)
        new_fluentLanguage = content.get('fluentLanguage', None)
        if new_fluentLanguage is None:
            abort(400)
        try:
            instructor = Instructor(
                         name=new_name,
                         teachLanguage=new_teachLanguage,
                         fluentLanguage=new_fluentLanguage)
            instructor.insert()
            instructors = Instructor.query.all()
            return jsonify({
                'success': True,
                'created': instructor.id,
                'totalInstructors': len(instructors)
                })
        except Exception:
            abort(400)

    @app.route('/instructor/<int:instructor_id>', methods=['PATCH'])
    @requires_auth('patch: instructor')
    def updateInstructor(instructor_id):
        instructor = Instructor.query.filter(
                     Instructor.id == instructor_id).one_or_none()
        if instructor is None:
            abort(404)
        content = request.get_json()
        instructor.name = content.get('name', None)
        instructor.teachLanguage = content.get('teachLanguage', None)
        instructor.fluentLanguage = content.get('fluentLanguage', None)
        instructor.update()
        return jsonify({
            "success": True,
            "name":  instructor.name,
            "teachLanguage": instructor.teachLanguage,
            "fluentLanguage": instructor.fluentLanguage
            })

    @app.route('/instructor/<int:instructor_id>', methods=['DELETE'])
    @requires_auth('delete: instructor')
    def deleteInstructor(instructor_id):
        try:
            instructor = Instructor.query.filter(
                         Instructor.id == instructor_id).one_or_none()
            if instructor is None:
                abort(404)
            instructor.delete()
            instructors = Instructor.query.all()
            return jsonify({
                'success': True,
                'totalInstructors': len(instructors)
                })
        except Exception:
            abort(404)

    @app.route('/instructorMatches/<int:student_id>', methods=['GET'])
    @requires_auth('get: instructorMatches')
    def instructorMatches(student_id):
        try:
            student = Student.query.filter(
                      Student.id == student_id).one_or_none()
            studyLanguage = student.studyLanguage
            nativeLanguage = student.nativeLanguage
            instructors = Instructor.query.filter(
                (Instructor.teachLanguage == studyLanguage) &
                (Instructor.fluentLanguage == nativeLanguage)).all()
            formatted_instructors = [instructor.format() for
                                     instructor in instructors]
            if formatted_instructors == []:
                abort(404)
            return jsonify({
                'success': True,
                'instructors': formatted_instructors,
                'totalMatchInstructors': len(instructors)
                })
        except Exception:
            abort(404)

# Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def authError(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error
        }), 403

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
