const MOCK_URL = {
    LOGIN: "https://private-d249a-pfeibm.apiary-mock.com/login",
    SIGN_UP: "https://private-d249a-pfeibm.apiary-mock.com/users",
    PROJECTS: "https://private-d249a-pfeibm.apiary-mock.com/users/$uid/projects",
    CREATE_PROJECT: "https://private-d249a-pfeibm.apiary-mock.com/projects",
    CLASSIFY: "http://private-d249a-pfeibm.apiary-mock.com/classify",
    USERS: "https://private-d249a-pfeibm.apiary-mock.com/projects/$pid/users",
    PROJECT: "https://private-d249a-pfeibm.apiary-mock.com/projects/$pid",
    ACCURACY: "https://private-d249a-pfeibm.apiary-mock.com/accuracy",
    ADD_USER: "https://private-d249a-pfeibm.apiary-mock.com/projects/$pid/users"
}

const DEV_URL = {
    LOGIN: "http://localhost:8000/api/v1/login",
    SIGN_UP: "http://localhost:8000/api/v1/users",
    PROJECTS: "http://localhost:8000/api/v1/users/$uid/projects",
    CREATE_PROJECT: "http://localhost:8000/api/v1/projects",
    CLASSIFY: "http://localhost:8000/api/v1/classify",
    USERS: "http://localhost:8000/api/v1/projects/$pid/users",
    PROJECT: "http://localhost:8000/api/v1/projects/$pid",
    ACCURACY: "http://localhost:8000/api/v1/accuracy",
    ADD_USER: "http://localhost:8000/api/v1/projects/$pid/users"
}

const PROD_URL = {
    // Change this URLs when backend goes to master
    LOGIN: "https://pfeinsper.mybluemix.net/api/v1/login",
    SIGN_UP: "https://pfeinsper.mybluemix.net/api/v1/users",
    PROJECTS: "https://pfeinsper.mybluemix.net/api/v1/users/$uid/projects",
    CREATE_PROJECT: "https://pfeinsper.mybluemix.net/api/v1/projects",
    CLASSIFY: "http://pfeinsper.mybluemix.net/api/v1/classify",
    USERS: "https://pfeinsper.mybluemix.net/api/v1/projects/$pid/users",
    PROJECT: "https://pfeinsper.mybluemix.net/api/v1/projects/$pid",
    ACCURACY: "https://pfeinsper.mybluemix.net/api/v1/accuracy",
    ADD_USER: "https://pfeinsper.mybluemix.net/api/v1/projects/$pid/users"
}

let URL

if (process.env.NODE_ENV === 'production') {
    URL = PROD_URL
} else {
    // Changes this do DEV_URL if using local backend
    URL = MOCK_URL
}

export default URL