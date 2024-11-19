# Flask Backend for Authentication and Animal Listings

This is a Flask backend application that provides authentication endpoints for user registration, login, and logout, as well as endpoints for managing animal listings. The application uses PostgreSQL as the database and Flask-SQLAlchemy for database interactions.

## Setup

1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install the required Python packages using pip:
     ```
     pip install -r requirements.txt
     ```

2. **Database Configuration**:
   - Ensure PostgreSQL is installed and running.
   - Create a new database and user in PostgreSQL:
     ```
     sudo -u postgres psql
     CREATE DATABASE my_phase5backend;
     CREATE USER my_username WITH ENCRYPTED PASSWORD 'my_password';
     GRANT ALL PRIVILEGES ON DATABASE my_phase5backend TO my_username;
     GRANT ALL PRIVILEGES ON SCHEMA public TO my_username;
     ```

3. **Run the Flask Application**:
   - Start the Flask application by running:
     ```
     python backend/app.py
     ```
   - The application will be available at `http://127.0.0.1:5000`.

## Testing with Postman

### Register a User

1. **Endpoint**: `POST /api/auth/register`
2. **URL**: `http://127.0.0.1:5000/api/auth/register`
3. **Request Body**:
   ```json
   {
     "name": "John Doe",
     "email": "john.doe@example.com",
     "password": "password123",
     "phone": "1234567890",
     "location": "New York",
     "role": "farmer"
   }
   ```
4. **Response**:
   - Status Code: `201 Created`
   - Body:
     ```json
     {
       "message": "User registered successfully"
     }
     ```

### Login a User

1. **Endpoint**: `POST /api/auth/login`
2. **URL**: `http://127.0.0.1:5000/api/auth/login`
3. **Request Body**:
   ```json
   {
     "email": "john.doe@example.com",
     "password": "password123"
   }
   ```
4. **Response**:
   - Status Code: `200 OK`
   - Body:
     ```json
     {
       "access_token": "your_jwt_token",
       "user": {
         "id": 1,
         "email": "john.doe@example.com",
         "name": "John Doe",
         "role": "farmer"
       }
     }
     ```

### Logout a User

1. **Endpoint**: `POST /api/auth/logout`
2. **URL**: `http://127.0.0.1:5000/api/auth/logout`
3. **Headers**:
   - `Authorization`: `Bearer your_jwt_token`
4. **Response**:
   - Status Code: `200 OK`
   - Body:
     ```json
     {
       "message": "Logout successful"
     }
     ```

### Create an Animal Listing

1. **Endpoint**: `POST /api/animals`
2. **URL**: `http://127.0.0.1:5000/api/animals`
3. **Headers**:
   - `Authorization`: `Bearer your_jwt_token`
4. **Request Body**:
   - Form Data:
     - `type`: `camel`
     - `breed`: `dromedary`
     - `age`: `24`
     - `price`: `1500`
     - `description`: `A healthy and strong dromedary camel.`
     - `images`: (file upload)
5. **How to Upload Files in Postman**:
   - In the Postman request, select the `Body` tab.
   - Choose `form-data`.
   - Add the fields as described above.
   - For the `images` field, select `File` instead of `Text`.
   - Click `Select Files` and choose the image files you want to upload.
6. **Response**:
   - Status Code: `201 Created`
   - Body:
     ```json
     {
       "message": "Animal created successfully",
       "animal": 1
     }
     ```

### Update an Animal Listing

1. **Endpoint**: `PUT /api/animals/<animal_id>`
2. **URL**: `http://127.0.0.1:5000/api/animals/1`
3. **Headers**:
   - `Authorization`: `Bearer your_jwt_token`
4. **Request Body**:
   - Form Data:
     - `type`: `camel`
     - `breed`: `dromedary`
     - `age`: `26`
     - `price`: `1600`
     - `description`: `A healthy and strong dromedary camel, slightly older.`
     - `images`: (file upload)
5. **How to Upload Files in Postman**:
   - In the Postman request, select the `Body` tab.
   - Choose `form-data`.
   - Add the fields as described above.
   - For the `images` field, select `File` instead of `Text`.
   - Click `Select Files` and choose the image files you want to upload.
6. **Response**:
   - Status Code: `200 OK`
   - Body:
     ```json
     {
       "message": "Animal updated successfully",
       "animal": 1
     }
     ```

### Delete an Animal Listing

1. **Endpoint**: `DELETE /api/animals/<animal_id>`
2. **URL**: `http://127.0.0.1:5000/api/animals/1`
3. **Headers**:
   - `Authorization`: `Bearer your_jwt_token`
4. **Response**:
   - Status Code: `200 OK`
   - Body:
     ```json
     {
       "message": "Animal deleted successfully"
     }
     ```

### Get Animal Listings

1. **Endpoint**: `GET /api/animals`
2. **URL**: `http://127.0.0.1:5000/api/animals`
3. **Headers**:
   - `Authorization`: `Bearer your_jwt_token`
4. **Response**:
   - Status Code: `200 OK`
   - Body:
     ```json
     [
       {
         "id": 1,
         "type": "camel",
         "breed": "dromedary",
         "age": 26,
         "price": 1600,
         "description": "A healthy and strong dromedary camel, slightly older.",
         "images": ["uploads/image1.jpg", "uploads/image2.jpg"],
         "status": "available"
       }
     ]
     ```

## Testing with cURL

### Register a User

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "phone": "1234567890",
  "location": "New York",
  "role": "farmer"
}'
```

### Login a User

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "password123"
}'
```

### Logout a User

```bash
curl -X POST http://127.0.0.1:5000/api/auth/logout \
-H "Authorization: Bearer your_jwt_token"
```

### Create an Animal Listing

```bash
curl -X POST http://127.0.0.1:5000/api/animals \
-H "Authorization: Bearer your_jwt_token" \
-F "type=camel" \
-F "breed=dromedary" \
-F "age=24" \
-F "price=1500" \
-F "description=A healthy and strong dromedary camel." \
-F "images=@path/to/image1.jpg" \
-F "images=@path/to/image2.jpg"
```

### Update an Animal Listing

```bash
curl -X PUT http://127.0.0.1:5000/api/animals/1 \
-H "Authorization: Bearer your_jwt_token" \
-F "type=camel" \
-F "breed=dromedary" \
-F "age=26" \
-F "price=1600" \
-F "description=A healthy and strong dromedary camel, slightly older." \
-F "images=@path/to/image1.jpg" \
-F "images=@path/to/image2.jpg"
```

### Delete an Animal Listing

```bash
curl -X DELETE http://127.0.0.1:5000/api/animals/1 \
-H "Authorization: Bearer your_jwt_token"
```

### Get Animal Listings

```bash
curl -X GET http://127.0.0.1:5000/api/animals \
-H "Authorization: Bearer your_jwt_token"
```

## Troubleshooting

- If you encounter a `psycopg2.errors.InsufficientPrivilege` error, ensure that the user has the necessary privileges on the `public` schema:
  ```
  GRANT ALL PRIVILEGES ON SCHEMA public TO my_username;
  ```

- If the Flask application fails to start, ensure that all dependencies are installed and the database connection string is correct.

## Additional Notes

- The application is running in debug mode. Do not use this in a production environment.
- The JWT secret key is set to `your_jwt_secret_key`. Change this to a secure secret key in a production environment.
