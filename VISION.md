# DUE TO MY INTERNSHIP, I AM UNABLE TO COMPLETE THIS PROJECT. 

# But My Vision for this project is : 

### Create two users:
 1. A OPS user
 2. A Client user

OPS User, would have routes like (op-login, op-upload)

While Client user would have routes like (client-login, client-download, client-upload, client-view)

My initial approach was to use a single database with two different collections, one for each user type.

But I am not sure if this is the best approach, since It would make redundunt columns for user types, like is_verified for my client user, and would be a security risk since I would have to map this to the uploaded-files table.


Using JWT Token for basic authentication.

For Sending mails I would use Celery and smtp or any API email client.
For Uploading files, I would use AWS S3 to prevent accesss to local filesystem.



It might not take much time to code with AI, but I find it unethical to use AI for this project, since it is a testing project.



##Routes Proposed
 ### Client Routes
     /client-login
     /client-register
     /client-register-verify/:verify-uuid
     /client-view (Authenticated)
     /client-download/:file-id (Authenticated)
 ### OPS Routes
     /ops-login
     /ops-upload (POST, Authenticated)
    
## Database Tables

    Client Table
        - id
        - email
        - password (hashed)
        - is_verified (boolean)
        - created_at
        - updated_at
    Ops Table
        - id
        - email
        - password (hashed)
        - created_at
        - updated_at

    Uploaded Files Table
        - id
        - file_name
        - file_path (S3 URL)
        - uploaded_by (Ops ID)
        - created_at
        - updated_at