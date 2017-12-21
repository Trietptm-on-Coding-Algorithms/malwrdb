class RefGroup{
    group_id: string;
    update_time: Date;
}

class RefDir{
    _id: string;
    dir_name: string;
}

class RefFile{
    file_name: string;
    file_size: number;
}

class Sample {
    sample_name: string;
    smaple_file_size: number;

    md5: string;
    sha1: string;
    sha128: string;
    sha256: string;
}



export { RefGroup, RefDir, RefFile, Sample };
