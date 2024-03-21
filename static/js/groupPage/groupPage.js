const uploadTable = () => {
  alert("테이블 업로드");
};

const shareTable = () => {
  alert("시간표 공유");
};

const saveImage = () => {
  alert("이미지 저장");
};

document.addEventListener("DOMContentLoaded", (event) => {
  let urlParts = window.location.href.split("/");
  let lastSegment = urlParts[urlParts.length - 1];
  let all_users = [];

  let min_num_of_people = parseInt(
    document.getElementsByClassName("filterinput")[0].value
  );
  let num_of_people_in_group;

  // 그룹에 속한 모든 유저 아이디 가져오기
  fetch(`http://127.0.0.1:8000/group/${lastSegment}`)
    .then((response) => response.json())
    .then((result) => {
      num_of_people_in_group = result.users.length;

      console.log(
        "그룹인원수, 최소인원수 : " +
          num_of_people_in_group +
          ", " +
          min_num_of_people
      );

      let m = num_of_people_in_group;
      let n = min_num_of_people;

      result.users.forEach((user) => {
        all_users.push(user.id);
      });

      let data = JSON.stringify({ ids: all_users });
      // 모든 유저에 대한 시간표 가져오기
      fetch(`http://127.0.0.1:8000/user/timetable`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: data,
      })
        .then((response) => response.json())
        .then((result) => {
          console.log(result);
          let tableElements = document.getElementsByClassName("tableElement");
          let days = {
            0: "mon",
            1: "tue",
            2: "wed",
            3: "thu",
            4: "fri",
            5: "sat",
            6: "sun",
          };

          // tableElements[index].style.backgroundColor = "#164DCA"; // 1순위
          // tableElements[index].style.backgroundColor = "#BDC5FF"; // 2순위
          // tableElements[index].style.backgroundColor = "#F0EDFF"; // 3순위

          for (let i = 0; i < 7; i++) {
            let day = result[days[i]];
            let day_impossibles_keys = Object.keys(day);
            for (let j = 0; j < day_impossibles_keys.length; j++) {
              let key = day_impossibles_keys[j];
              console.log(days[i] + key);
              let cell_impossible_people = day[key];
              let possible = m - cell_impossible_people.length;

              let index = i + 7 * (key - 1);
              if (index < 63) {
                // if (m - n >= 2) {
                //   if (possible >= n + 2)
                //     tableElements[index].style.backgroundColor = "#164DCA";
                //   // 1순위
                //   else if (possible == n + 1)
                //     tableElements[index].style.backgroundColor = "#BDC5FF";
                //   // 2순위
                //   else if (possible == n)
                //     tableElements[index].style.backgroundColor = "#F0EDFF"; // 3순위
                // } else if (m - n == 1) {
                //   if (possible == n + 1)
                //     tableElements[index].style.backgroundColor = "#164DCA";
                //   // 1순위
                //   else if (possible == n)
                //     tableElements[index].style.backgroundColor = "#BDC5FF";
                //   // 2순위
                //   else
                //     document.getElementsByClassName("priority")[2].innerHTML =
                //       "불가처리";
                // } else if (m - n == 0) {
                //   if (possible == n)
                //     tableElements[index].style.backgroundColor = "#164DCA"; // 1순위
                // }
              }
            }
          }
        });
    });
});
