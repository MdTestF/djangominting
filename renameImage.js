    
const { resolve } = require('path');
const { readdirSync, rename,} = require('fs');
const basePath = process.cwd();
const buildDir = `${basePath}/build/images`;
const imageDirPath1 = resolve(buildDir, '');


const imagerename = ()=>{
    const files1 = readdirSync(imageDirPath1);
    files1.forEach((file,i)=> {

        let filename =file.split(".")
        if(i===0){
            i=1
        }else{
            i=i+1;
        }
        let name =i
        let ext = filename[filename.length-1]
        console.log(ext)
        rename(
            imageDirPath1 + `/${file}`,
            imageDirPath1 + `/`+name+'.'+ext,
            err => console.log(err)
          )
    }
    
      );

}

imagerename()

