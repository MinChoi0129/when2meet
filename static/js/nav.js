
class Nav {
    constructor() {
        this.checkUserLogin();
        this.clickLogin();
        this.clickClose();
        this.clickMenu();
        this.clickMenuClose();
    }
    checkIfUserIsLoggedIn() {
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        const accessTokenCookie = cookies.find(cookie => cookie.startsWith('access_token='));
        return accessTokenCookie !== undefined;
    }
    
    checkUserLogin() {
        const isLoggedIn = this.checkIfUserIsLoggedIn();

        if (isLoggedIn) {
            // 사용자가 로그인 상태인 경우
            document.querySelector('.beforeLogin').classList.add('unactive');
            document.querySelector('.afterLogin').classList.remove('unactive');
        } else {
            // 사용자가 로그아웃 상태인 경우
            document.querySelector('.beforeLogin').classList.remove('unactive');
            document.querySelector('.afterLogin').classList.add('unactive');
        }
    }

     /* nav.html 로그인 클릭 이벤트 */
     clickLogin() {
        const loginBtn = document.querySelector('.login')
        loginBtn.addEventListener('click', () => {
                document.querySelector('.loginModal').classList.remove('unactive')
            })
        ;console.log("hi")
    }

    /* login.html x 클릭 이벤트 */
    clickClose(){
        let closeBtn = document.querySelector('.closeBtn')
        closeBtn.addEventListener('click',()=>{
            document.querySelector('.loginModal').classList.add('unactive')

        })
    }

    /* menu.html 클릭 이벤트 */
    clickMenu(){
        const groupinBtn = document.querySelector('.menu')
        groupinBtn.addEventListener('click',()=>{
            document.querySelector('.menuModal').classList.remove('unactive')
            
        })
    }
    /* menu.html x 클릭 이벤트 */
    clickMenuClose(){
        let closeBtn = document.querySelectorAll('.closeBtn')
        closeBtn[1].addEventListener('click',()=>{
            document.querySelector('.menuModal').classList.add('unactive')

        })
    }




}



window.addEventListener('load', function() {
    new Nav();
    });