/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

import expect from 'expect';
import lolex from 'lolex';
import { describe, it } from 'mocha';

import { timeDelta } from './time';


describe('timeDelta', () => {
  it('returns an empty structure for invalid datetimes', () => {
    const undefinedDelta = {
      isFuture: null,
      seconds: null,
      minutes: null,
      hours: null,
      days: null,
      weeks: null,
      months: null,
      years: null,
    };
    expect(timeDelta('')).toEqual(undefinedDelta);
    expect(timeDelta(null)).toEqual(undefinedDelta);
    expect(timeDelta(undefined)).toEqual(undefinedDelta);
    expect(timeDelta('Invalid')).toEqual(undefinedDelta);
    expect(timeDelta('2016-14-12')).toEqual(undefinedDelta);
    expect(timeDelta('2016-12-12 25:02:11')).toEqual(undefinedDelta);
  });

  describe('positive duration', () => {
    const tests = [
      {
        unit: 'seconds',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2016-07-07T00:00:44+00:00'],
        expected: {
          isFuture: true,
          seconds: 44,
          minutes: 0,
          hours: 0,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'seconds (TZ-aware)',
        now: '2016-07-07T00:00:00+02:00',
        args: ['2016-07-06T22:00:44+00:00'],
        expected: {
          isFuture: true,
          seconds: 44,
          minutes: 0,
          hours: 0,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'minutes',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2016-07-07T00:59:00+00:00'],
        expected: {
          isFuture: true,
          seconds: 3540,
          minutes: 59,
          hours: 0,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'minutes (TZ-aware)',
        now: '2016-07-07T00:00:00+02:00',
        args: ['2016-07-06T22:59:00+00:00'],
        expected: {
          isFuture: true,
          seconds: 3540,
          minutes: 59,
          hours: 0,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'hours',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2016-07-07T23:00:44+00:00'],
        expected: {
          isFuture: true,
          seconds: 82844,
          minutes: 1380,
          hours: 23,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'hours (TZ-aware)',
        now: '2016-07-07T00:00:00+02:00',
        args: ['2016-07-07T21:00:44+00:00'],
        expected: {
          isFuture: true,
          seconds: 82844,
          minutes: 1380,
          hours: 23,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'days',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2016-07-13T23:59:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 604799,
          minutes: 10079,
          hours: 167,
          days: 6,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'days (TZ-aware)',
        now: '2016-07-07T00:00:00+02:00',
        args: ['2016-07-13T21:59:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 604799,
          minutes: 10079,
          hours: 167,
          days: 6,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'weeks',
        now: '2016-06-27T23:59:59+00:00',
        args: ['2016-07-07T00:00:00+00:00'],
        expected: {
          isFuture: true,
          seconds: 777601,
          minutes: 12960,
          hours: 216,
          days: 9,
          weeks: 1,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'weeks (TZ-aware)',
        now: '2016-06-27T21:59:59+00:00',
        args: ['2016-07-07T00:00:00+02:00'],
        expected: {
          isFuture: true,
          seconds: 777601,
          minutes: 12960,
          hours: 216,
          days: 9,
          weeks: 1,
          months: 0,
          years: 0,
        },
      },
      {
        unit: 'months',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2016-10-07T23:59:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 8035199,
          minutes: 133919,
          hours: 2231,
          days: 92,
          weeks: 13,
          months: 3, // 1 month ~30 days
          years: 0,
        },
      },
      {
        unit: 'months (TZ-aware)',
        now: '2016-07-07T00:00:00+02:00',
        args: ['2016-10-07T21:59:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 8035199,
          minutes: 133919,
          hours: 2231,
          days: 92,
          weeks: 13,
          months: 3, // 1 month ~30 days
          years: 0,
        },
      },
      {
        unit: 'years',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2017-07-07T00:00:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 31536059,
          minutes: 525600,
          hours: 8760,
          days: 365,
          weeks: 52,
          months: 12,
          years: 1,
        },
      },
      {
        unit: 'years (TZ-aware)',
        now: '2016-07-07T00:00:00+00:00',
        args: ['2017-07-07T00:00:59+00:00'],
        expected: {
          isFuture: true,
          seconds: 31536059,
          minutes: 525600,
          hours: 8760,
          days: 365,
          weeks: 52,
          months: 12,
          years: 1,
        },
      },
    ];

    tests.forEach((test) => {
      it(`calculates ${test.unit} of difference`, () => {
        lolex.install(Date.parse(test.now));
        expect(timeDelta(...test.args)).toEqual(test.expected);
      });
    });
  });

  describe('negative duration (times in the future)', () => {
    const tests = [
      {
        unit: 'seconds',
        now: '2016-07-07T00:00:44+00:00',
        args: ['2016-07-07T00:00:00+00:00'],
        expected: {
          isFuture: false,
          seconds: 44,
          minutes: 0,
          hours: 0,
          days: 0,
          weeks: 0,
          months: 0,
          years: 0,
        },
      },
    ];

    tests.forEach((test) => {
      it(`calculates ${test.unit} of difference`, () => {
        lolex.install(Date.parse(test.now));
        expect(timeDelta(...test.args)).toEqual(test.expected);
      });
    });
  });
});
