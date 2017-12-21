import { Component, OnInit, Input } from '@angular/core';

import { RefDir, Sample, RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

import { RefFileComponent } from './ref-file.component';
import { SampleComponent } from './sample.component';

@Component({
  selector: 'ref-dir',

  template: `
    <div *ngIf="subRefDirs">
        <div *ngFor="let dir of subRefDirs">
            <p>{{ dir.dir_name }}</p>
            <ref-dir [refDir]="dir"></ref-dir>
        </div>
    </div>
    <div *ngIf="subSamples">
        <div *ngFor="let sample of subSamples">
            <p>{{ sample.md5 }}</p>
            <sample [sample]="sample"></sample>
        </div>
    </div>
    <div *ngIf="subRefFiles">
        <div *ngFor="let file of subRefFiles">
            <p>{{ file.md5 }}</p>
            <ref-file [refFile]="file"></ref-file>
        </div>
    </div>
  `
})

export class RefDirComponent implements OnInit {
  @Input() refDir: RefDir;
  subRefDirs: RefDir[];
  subSamples: Sample[];
  subRefFiles: RefFile[];
  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
      // console.log("id:" + this.refDir._id);
      this._svrdata.getSubRefDirs(this.refDir._id).subscribe(
        v => {
          this.subRefDirs = v;
        },
        e => { console.log("getSubRefDirs error: " + e); },
        () => { }
      );
      this._svrdata.getSubSamples(this.refDir._id).subscribe(
          v => {
            this.subSamples = v;
          },
          e => { console.log("getSubSamples error: " + e); },
          () => { }
      );
      this._svrdata.getSubRefFiles(this.refDir._id).subscribe(
          v => {
            this.subRefFiles = v;
          },
          e => { console.log("getSubRefFiles error: " + e); },
          () => { }
      );
  }
}
