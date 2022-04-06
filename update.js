const axios = require('axios');
const fs = require('fs');


let rawdata = fs.readFileSync(`./build/json/_metadata.json`);
let data = JSON.parse(rawdata);

data.forEach(async(item) => {
    
    const res = await axios.get('http://127.0.0.1:8000/api/getClickUp')
    // console.log('./media/'+res.data) 

    const res1 =await axios.post('http://127.0.0.1:8000/api/getCID/',{img:res.data},{
        headers:{
            'Content-Type':'application/json'
        }}
    );

    console.log(item.image)

    let file =item.image.split("/")
    // console.log()
    let name = file[file.length-1]
    let suf =name.split(".")
    console.log(suf)


    item.image = `${'ipfs://'+res1.data}/${file[file.length-1]}`;
    let imgname = res.data.split("_")

    item.name = imgname[1];

    console.log(item.image)
   
    fs.writeFileSync(
     `build/json/${suf[0]}.json`,
      JSON.stringify(item, null, 2)
    );

    fs.writeFileSync(
      `build/json/_metadata.json`,
      JSON.stringify(data, null, 2)
    );
  });
  



  