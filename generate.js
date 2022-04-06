const fs = require("fs");
const path = require("path");
const {loadImage } = require("canvas");
const basePath = process.cwd();
const buildDir = `${basePath}/build/json`;
const inputDir = `${basePath}/build/images`;
const axios = require('axios');
const namePrefix = "Your Collection";
const description = "Remember to replace this description";
const baseUri = "ipfs://";
const console = require("console");
const { async } = require("recursive-fs/lib/copy");
const metadataList = [];

const buildSetup = () => {
  if (fs.existsSync(buildDir)) {
    fs.rmSync(buildDir, { recursive: true });
  }
  fs.mkdirSync(buildDir);
};

const getImages = (_dir) => {
  try {
    return fs
      .readdirSync(_dir)
      .filter((item) => {
        return item;  
      })
      .map((i) => {
        return {
          filename: i,
          path: `${_dir}/${i}`,
        };
      });
  } catch {
    return null;
  }
};

const loadImgData = async (_imgObject) => {
  try {
    const image = await loadImage(`${_imgObject.path}`);
   
    return {
      imgObject: _imgObject,
      loadedImage: image,
    };
  } catch (error) {
    console.error("Error loading image:", error);
  }
};



const saveMetadata = async(_loadedImageObject) => {
  let tempAttributes = [];
  let name = _loadedImageObject.imgObject.filename
  console.log(name)
  let file =name.split(".")
  console.log(file)
  imageName = file[0]
  console.log(imageName)

  let tempMetadata = {
    name: `${namePrefix}`,
    description: description,
    image: `${baseUri}/${_loadedImageObject.imgObject.filename}`,
    //edition: Number(shortName),
    attributes: tempAttributes,
  };

  metadataList.push(tempMetadata);
  fs.writeFileSync(
    `${buildDir}/${imageName}.json`,
    JSON.stringify(tempMetadata, null, 2)
  );
  
};

const writeMetaData = (_data) => {
  fs.writeFileSync(`${buildDir}/_metadata.json`, _data);
};

const startCreating = async () => {
  const images = getImages(inputDir);
  if (images == null) {
    console.log("Please generate collection first.");
    return;
  }
  let loadedImageObjects = [];
  images.forEach((imgObject) => {
    loadedImageObjects.push(loadImgData(imgObject));
  });
  await Promise.all(loadedImageObjects).then((loadedImageObjectArray) => {
    loadedImageObjectArray.forEach((loadedImageObject) => {
      saveMetadata(loadedImageObject);
      console.log(
        `Created metadata for image: ${loadedImageObject.imgObject.filename}`
      );
    });
  });
  writeMetaData(JSON.stringify(metadataList, null, 2));
};

buildSetup();
startCreating();
