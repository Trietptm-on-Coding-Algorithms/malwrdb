import { NgModule } from '@angular/core';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@NgModule({
  imports: [MatGridListModule, MatButtonModule, MatProgressBarModule],
  exports: [MatGridListModule, MatButtonModule, MatProgressBarModule],
})
export class MaterialComponentModule { }
