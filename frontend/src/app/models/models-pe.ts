class PeSample {
    _id: string;
}

class PeValueStructure {
  name: string;
  fileOffset: number;
  mmOffset: number;
  value: string;
}

class PeDosHeader {
  values_list: Array<PeValueStructure>;
}


class PeFileHeader{

}

class PeNtHeader{

}


export { PeSample, PeDosHeader, PeFileHeader, PeNtHeader }