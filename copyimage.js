    
const fs = require('fs');
const { resolve } = require('path');
const { readdirSync} = require('fs');
const { async } = require('recursive-fs/lib/copy');
const basePath = process.cwd();
const buildDir1 = `${basePath}/media`;
const buildDir = `${basePath}/build/images`;
const imageDirPath = resolve(buildDir1, '');
const files = readdirSync(imageDirPath);
const axios = require('axios');


const buildSetup = () => {
    if (fs.existsSync(buildDir)) {
      fs.rmSync(buildDir, { recursive: true });
    }
    fs.mkdirSync(buildDir);
  };

  
  



const imageCopy=async()=>{

    const res=await axios.get('http://127.0.0.1:8000/api/getClickUp')
    console.log(res.data)

    files.forEach((file)=>{

        if(file===res.data){
    
            const filePath =  `./media/${file}`;
            const filePathCopy = `./build/images/${file}`;
        
        fs.copyFile(filePath, filePathCopy, (err) => {
            if (err) throw err;
            console.log('File Copy Successfully.');
        });
    
        }   
    
    });

}


buildSetup();
imageCopy()



