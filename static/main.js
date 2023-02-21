let prev = 0;
setInterval(()=>{
    fetch('/css-refresher').then((resp)=>resp.json()).then((resp)=>{
        console.log(resp);
        let curr = resp["css_change_count"];
        if (prev < curr) {
            prev = curr;
            $("body").load(location.href);
        }
    })
  }, 1000);