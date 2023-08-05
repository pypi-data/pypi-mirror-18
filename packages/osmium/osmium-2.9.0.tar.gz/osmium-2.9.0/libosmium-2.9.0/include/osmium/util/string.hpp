#ifndef OSMIUM_UTIL_STRING_HPP
#define OSMIUM_UTIL_STRING_HPP

/*

This file is part of Osmium (http://osmcode.org/libosmium).

Copyright 2013-2016 Jochen Topf <jochen@topf.org> and others (see README).

Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

*/

#include <cstddef>
#include <string>
#include <vector>

namespace osmium {

    /**
     * Split string on the separator character.
     *
     * @param str The string to be split.
     * @param sep The separator character.
     * @param compact Set this to true to remove empty strings from result
     * @returns Vector with the parts of the string split up.
     */
    inline std::vector<std::string> split_string(const std::string& str, const char sep, bool compact = false) {
        std::vector<std::string> tokens;

        if (!str.empty()) {
            size_t pos = 0;
            size_t nextpos = str.find_first_of(sep);
            while (nextpos != std::string::npos) {
                if (!compact || (nextpos - pos != 0)) {
                    tokens.push_back(str.substr(pos, nextpos-pos));
                }
                pos = nextpos + 1;
                nextpos = str.find_first_of(sep, pos);
            }
            if (!compact || pos != str.size()) {
                tokens.push_back(str.substr(pos));
            }
        }

        return tokens;
    }

    /**
     * Split string on the separator character(s).
     *
     * @param str The string to be split.
     * @param sep The separator character(s).
     * @param compact Set this to true to remove empty strings from result
     * @returns Vector with the parts of the string split up.
     */
    inline std::vector<std::string> split_string(const std::string& str, const char* sep, bool compact = false) {
        std::vector<std::string> tokens;

        if (!str.empty()) {
            size_t pos = 0;
            size_t nextpos = str.find_first_of(sep);
            while (nextpos != std::string::npos) {
                if (!compact || (nextpos - pos != 0)) {
                    tokens.push_back(str.substr(pos, nextpos-pos));
                }
                pos = nextpos + 1;
                nextpos = str.find_first_of(sep, pos);
            }
            if (!compact || pos != str.size()) {
                tokens.push_back(str.substr(pos));
            }
        }

        return tokens;
    }

} // namespace osmium

#endif // OSMIUM_UTIL_STRING_HPP
