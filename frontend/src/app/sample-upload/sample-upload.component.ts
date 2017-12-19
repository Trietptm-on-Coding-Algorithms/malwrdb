import { Component, OnInit } from '@angular/core';

import { MaterialComponentModule } from '../modules/material-component.module';
import { FileUploader } from './upload';

// 变量
const URL = 'http://127.0.0.1:5000/sample/upload/';

@Component({
  selector: 'sample-upload',
  templateUrl: './sample-upload.component.html',
  styleUrls: ['./sample-upload.component.css']
})
export class SampleUploadComponent {

  public sample_uploader: FileUploader = new FileUploader({ url: URL });
  public group_uploader: FileUploader = new FileUploader({ url: URL });
  public hasBaseDropZoneOver: boolean = false;
  public hasAnotherDropZoneOver: boolean = false;

  public fileOverBase(e: any): void {
    this.hasBaseDropZoneOver = e;
  }

  public fileOverAnother(e: any): void {
    this.hasAnotherDropZoneOver = e;
  }
}
