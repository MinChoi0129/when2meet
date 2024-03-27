
class Signup {
    constructor() {
        this.clickRegist();
    }


    clickRegist(){
        const registBtn = document.querySelector('.btn-primary');
        registBtn.addEventListener('click',()=>{
            this.post_user(userForm);
        })
    }
    post_user(userForm){
        userForm.preventDefault()
        const createUrl = "/user/create"
        const datas = {
            id :id,
            pw:pw,
            birthDay:birthDay,
            email:email,
            pw2:pw,
            img:img
        }

        fastapi('post', createUrl, datas, 
        (json) => {
            push('/')
        },
        (json_error) => {
            error = json_error
        }
    )
    }
}

window.onload = () => {
    new Signup();
};


    