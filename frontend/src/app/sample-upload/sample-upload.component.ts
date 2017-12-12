import { Component, OnInit } from '@angular/core';
import { FileUploader } from './upload'

const URL = 'http://127.0.0.1:5000/sample_upload/';

@Component({
  selector: 'sample-upload',
  templateUrl: './sample-upload.component.html',
  styleUrls: ['./sample-upload.component.css']
})
export class SampleUploadComponent {

  constructor() { }

  public uploader: FileUploader = new FileUploader({url: URL});
}
