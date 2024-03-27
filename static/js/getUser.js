export class GetUser {
    constructor() {
        // 현재 로그인 유저 아이디
        this.whoThisUser = null;
        this.getCookie();
    }

    getCookie() {
        console.log("겟쿠키확인");
        if (document.cookie) {
            const cookies = document.cookie.split(`; `).map((el) => el.split('='));
            if (cookies.length > 0) {
                let getItem = [];
                for (let i = 0; i < cookies.length; i++) {
                    getItem.push(cookies[i][1]);
                }
                if (getItem.length > 0) {
                    console.log(getItem);
                    for (let i = 0; i < getItem.length; i++) {
                        const cookieParts = getItem[i].split('.');
                        if (cookieParts.length === 3) {
                            const [headerB64, payloadB64, signature] = cookieParts;
                            const headers = JSON.parse(atob(headerB64));
                            const payload = JSON.parse(atob(payloadB64));
                            
                            // payload에 있는 sub 값으로 whoThisUser 설정
                            this.whoThisUser = payload.sub;

                            console.log(headers);
                            console.log(payload);
                            console.log(signature);
                        } 
                    }
                } 
            } 
        } 
    }
}
