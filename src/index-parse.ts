#!/usr/bin/env node

import * as args from 'args';
import App from './App';

args
  .command('parse', 'Parse Smogon usage stats data')
  .option('date', 'The date to parse Smogon data for.')
  .option('format', 'The format to parse Smogon data for.')
  .option('rating', 'The rating to parse Smogon data for.');

const flags = args.parse(process.argv);

const app = new App(flags);
app.parse();
