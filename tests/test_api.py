import unittest
from app import create_app, db
from app.models import User, Role 

class APITest(unittest):
    
    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def test_posts(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='john@example.com', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_auth_header('john@example.com', 'cat'),
            data=json.dumps({'body': 'body of the *blog* post'})
        )
        self.assertTrue(response.status_code == 200)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        response = self.client.get(
            url,
            headers=self.get_auth_header('john@example.com', 'cat')
        )
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['body'] == 'body of the *body* post')
        self.assertTrue(json_response['body_html'] == '<p>body of the <em>blog</em> post</p>')




        
