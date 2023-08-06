Release History
===============


### 1.2.0 (2016-11-16)

**New Features**

- Migration of ownership to personal Github account for continued support and enhancements
- Update of documentation for easier readability on both github and pypi
- Development enhancements to use virtualenv versus system python environment

### 1.1.2 (2016-09-29)

**New Features**

- A more comprehensive set of Validation methods for evaluating things like (i) response codes, (ii) response content, (iii) response headers, and (iv) time-to-last-byte (ttlb)
- Adding better assertion debug messages for determining what failed and why. For example: `http://www.google.com/foobar - 200 == 301`, which basically means that the request to `http://www.google.com/foobar` failed because we were expecting `200` but got a `301`
- Adding several unit-tests for ensuring the code continues to work

### 1.0.0 (2016-06-01)

**New Features**

- First release of requestests testing tool for the world