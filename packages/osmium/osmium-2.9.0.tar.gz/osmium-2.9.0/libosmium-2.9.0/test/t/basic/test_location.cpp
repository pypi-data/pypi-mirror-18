#include "catch.hpp"

#include <sstream>
#include <type_traits>

#include <osmium/osm/location.hpp>

TEST_CASE("Location") {

// fails on MSVC and doesn't really matter
// static_assert(std::is_literal_type<osmium::Location>::value, "osmium::Location not literal type");

    SECTION("instantiation_with_default_parameters") {
        osmium::Location loc;
        REQUIRE(!loc);
        REQUIRE_THROWS_AS(loc.lon(), osmium::invalid_location);
        REQUIRE_THROWS_AS(loc.lat(), osmium::invalid_location);
    }

    SECTION("instantiation_with_double_parameters") {
        osmium::Location loc1(1.2, 4.5);
        REQUIRE(!!loc1);
        REQUIRE(12000000 == loc1.x());
        REQUIRE(45000000 == loc1.y());
        REQUIRE(1.2 == loc1.lon());
        REQUIRE(4.5 == loc1.lat());

        osmium::Location loc2(loc1);
        REQUIRE(4.5 == loc2.lat());

        osmium::Location loc3 = loc1;
        REQUIRE(4.5 == loc3.lat());
    }

    SECTION("instantiation_with_double_parameters_constructor_with_universal_initializer") {
        osmium::Location loc { 2.2, 3.3 };
        REQUIRE(2.2 == loc.lon());
        REQUIRE(3.3 == loc.lat());
    }

    SECTION("instantiation_with_double_parameters_constructor_with_initializer_list") {
        osmium::Location loc({ 4.4, 5.5 });
        REQUIRE(4.4 == loc.lon());
        REQUIRE(5.5 == loc.lat());
    }

    SECTION("instantiation_with_double_parameters_operator_equal") {
        osmium::Location loc = { 5.5, 6.6 };
        REQUIRE(5.5 == loc.lon());
        REQUIRE(6.6 == loc.lat());
    }

    SECTION("equality") {
        osmium::Location loc1(1.2, 4.5);
        osmium::Location loc2(1.2, 4.5);
        osmium::Location loc3(1.5, 1.5);
        REQUIRE(loc1 == loc2);
        REQUIRE(loc1 != loc3);
    }

    SECTION("order") {
        REQUIRE(osmium::Location(-1.2, 10.0) < osmium::Location(1.2, 10.0));
        REQUIRE(osmium::Location(1.2, 10.0) > osmium::Location(-1.2, 10.0));

        REQUIRE(osmium::Location(10.2, 20.0) < osmium::Location(11.2, 20.2));
        REQUIRE(osmium::Location(10.2, 20.2) < osmium::Location(11.2, 20.0));
        REQUIRE(osmium::Location(11.2, 20.2) > osmium::Location(10.2, 20.0));
    }

    SECTION("validity") {
        REQUIRE(osmium::Location(0.0, 0.0).valid());
        REQUIRE(osmium::Location(1.2, 4.5).valid());
        REQUIRE(osmium::Location(-1.2, 4.5).valid());
        REQUIRE(osmium::Location(-180.0, -90.0).valid());
        REQUIRE(osmium::Location(180.0, -90.0).valid());
        REQUIRE(osmium::Location(-180.0, 90.0).valid());
        REQUIRE(osmium::Location(180.0, 90.0).valid());

        REQUIRE(!osmium::Location(200.0, 4.5).valid());
        REQUIRE(!osmium::Location(-1.2, -100.0).valid());
        REQUIRE(!osmium::Location(-180.0, 90.005).valid());
    }


    SECTION("output_to_iterator_comma_separator") {
        char buffer[100];
        osmium::Location loc(-3.2, 47.3);
        *loc.as_string(buffer, ',') = 0;
        REQUIRE(std::string("-3.2,47.3") == buffer);
    }

    SECTION("output_to_iterator_space_separator") {
        char buffer[100];
        osmium::Location loc(0.0, 7.0);
        *loc.as_string(buffer, ' ') = 0;
        REQUIRE(std::string("0 7") == buffer);
    }

    SECTION("output_to_iterator_check_precision") {
        char buffer[100];
        osmium::Location loc(-179.9999999, -90.0);
        *loc.as_string(buffer, ' ') = 0;
        REQUIRE(std::string("-179.9999999 -90") == buffer);
    }

    SECTION("output_to_iterator_undefined_location") {
        char buffer[100];
        osmium::Location loc;
        REQUIRE_THROWS_AS(loc.as_string(buffer, ','), osmium::invalid_location);
    }

    SECTION("output_to_string_comman_separator") {
        std::string s;
        osmium::Location loc(-3.2, 47.3);
        loc.as_string(std::back_inserter(s), ',');
        REQUIRE(s == "-3.2,47.3");
    }

    SECTION("output_to_string_space_separator") {
        std::string s;
        osmium::Location loc(0.0, 7.0);
        loc.as_string(std::back_inserter(s), ' ');
        REQUIRE(s == "0 7");
    }

    SECTION("output_to_string_check_precision") {
        std::string s;
        osmium::Location loc(-179.9999999, -90.0);
        loc.as_string(std::back_inserter(s), ' ');
        REQUIRE(s == "-179.9999999 -90");
    }

    SECTION("output_to_string_undefined_location") {
        std::string s;
        osmium::Location loc;
        REQUIRE_THROWS_AS(loc.as_string(std::back_inserter(s), ','), osmium::invalid_location);
    }

    SECTION("output_defined") {
        osmium::Location p(-3.20, 47.30);
        std::stringstream out;
        out << p;
        REQUIRE(out.str() == "(-3.2,47.3)");
    }

    SECTION("output_undefined") {
        osmium::Location p;
        std::stringstream out;
        out << p;
        REQUIRE(out.str() == "(undefined,undefined)");
    }

}

TEST_CASE("Location hash") {
    if (sizeof(size_t) == 8) {
        REQUIRE(std::hash<osmium::Location>{}({0, 0}) == 0);
        REQUIRE(std::hash<osmium::Location>{}({0, 1}) == 1);
        REQUIRE(std::hash<osmium::Location>{}({1, 0}) == 0x100000000);
        REQUIRE(std::hash<osmium::Location>{}({1, 1}) == 0x100000001);
    } else {
        REQUIRE(std::hash<osmium::Location>{}({0, 0}) == 0);
        REQUIRE(std::hash<osmium::Location>{}({0, 1}) == 1);
        REQUIRE(std::hash<osmium::Location>{}({1, 0}) == 1);
        REQUIRE(std::hash<osmium::Location>{}({1, 1}) == 0);
    }
}

#define CR(s, v, r) { \
                const char* strm = "-" s; \
                const char* strp = strm + 1; \
                REQUIRE(std::atof(strp) == Approx( v / 10000000.0)); \
                REQUIRE(std::atof(strm) == Approx(-v / 10000000.0)); \
                const char** data = &strp; \
                REQUIRE(osmium::detail::string_to_location_coordinate(data) == v); \
                REQUIRE(std::string{*data} == r); \
                data = &strm; \
                REQUIRE(osmium::detail::string_to_location_coordinate(data) == -v); \
                REQUIRE(std::string{*data} == r); \
                }

#define C(s, v) CR(s, v, "")

#define F(s) { \
             const char* strm = "-" s; \
             const char* strp = strm + 1; \
             const char** data = &strp; \
             REQUIRE_THROWS_AS(osmium::detail::string_to_location_coordinate(data), osmium::invalid_location); \
             data = &strm; \
             REQUIRE_THROWS_AS(osmium::detail::string_to_location_coordinate(data), osmium::invalid_location); \
             }

TEST_CASE("Parsing coordinates from strings") {
    F("x");
    F(".");
    F("--");
    F("");
    F(" ");
    F(" 123");

    CR("123 ", 1230000000, " ");
    CR("123x", 1230000000, "x");
    CR("1.2x",   12000000, "x");

    C("0",              0);

    C("1",       10000000);
    C("2",       20000000);

    C("9",       90000000);
    C("10",     100000000);
    C("11",     110000000);

    C("90",     900000000);
    C("100",   1000000000);
    C("101",   1010000000);

    C("00",             0);
    C("01",      10000000);
    C("001",     10000000);
    C("0001",    10000000);

    F("1234");
    F("1234.");
    F("12345678901234567890");

    C("0.",             0);
    C("0.0",            0);
    C("1.",      10000000);
    C("1.0",     10000000);
    C("1.2",     12000000);
    C("0.1",      1000000);
    C("0.01",      100000);
    C("0.001",      10000);
    C("0.0001",      1000);
    C("0.00001",      100);
    C("0.000001",      10);
    C("0.0000001",      1);

    C("1.1234567",  11234567);
    C("1.12345670", 11234567);
    C("1.12345674", 11234567);
    C("1.123456751", 11234568);
    C("1.12345679", 11234568);
    C("1.12345680", 11234568);
    C("1.12345681", 11234568);

    C("180.0000000",  1800000000);
    C("180.0000001",  1800000001);
    C("179.9999999",  1799999999);
    C("179.99999999", 1800000000);
    C("200.123",      2001230000);

    C("1e2",   1000000000);
    C("1e1",    100000000);
    C("1e0",     10000000);
    C("1e-1",     1000000);
    C("1e-2",      100000);
    C("1e-3",       10000);
    C("1e-4",        1000);
    C("1e-5",         100);
    C("1e-6",          10);
    C("1e-7",           1);

    C("1.0e2",   1000000000);
    C("1.1e1",    110000000);
    C("0.1e1",     10000000);
    C("1.2e0",     12000000);
    C("1.9e-1",     1900000);
    C("2.0e-2",      200000);
    C("2.1e-3",       21000);
    C("9.0e-4",        9000);
    C("9.1e-5",         910);
    C("1.0e-6",          10);
    C("1.0e-7",           1);
    C("1.4e-7",           1);
    C("1.5e-7",           2);
    C("1.9e-7",           2);
    C("0.5e-7",           1);
    C("0.1e-7",           0);
    C("0.0e-7",           0);
    C("1.9e-8",           0);
    C("1.9e-9",           0);
    C("1.9e-10",          0);

    F("e");
    F(" e");
    F(" 1.1e2");
    F("1.0e3");
    F("5e4");
    F("5.0e2");
    F("3e2");
    F("1e");
    F("0.5e");
    F("1e10");

    CR("1e2 ",   1000000000, " ");
    CR("1.1e2 ", 1100000000, " ");
    CR("1.1e2x", 1100000000, "x");
    CR("1.1e2:", 1100000000, ":");
}

#undef C
#undef CR
#undef F

#define CW(v, s) buffer.clear(); \
                 osmium::detail::append_location_coordinate_to_string(std::back_inserter(buffer), v); \
                 CHECK(buffer == s); \
                 buffer.clear(); \
                 osmium::detail::append_location_coordinate_to_string(std::back_inserter(buffer), -v); \
                 CHECK(buffer == "-" s);

TEST_CASE("Writing coordinates into string") {
    std::string buffer;

    osmium::detail::append_location_coordinate_to_string(std::back_inserter(buffer), 0);
    CHECK(buffer == "0");

    CW(  10000000, "1");
    CW(  90000000, "9");
    CW( 100000000, "10");
    CW(1000000000, "100");
    CW(2000000000, "200");

    CW(   1000000, "0.1");
    CW(    100000, "0.01");
    CW(     10000, "0.001");
    CW(      1000, "0.0001");
    CW(       100, "0.00001");
    CW(        10, "0.000001");
    CW(         1, "0.0000001");

    CW(   1230000, "0.123");
    CW(   9999999, "0.9999999");
    CW(  40101010, "4.010101");
    CW( 494561234, "49.4561234");
    CW(1799999999, "179.9999999");
}

#undef CW

TEST_CASE("set lon/lat from string") {
    osmium::Location loc;
    loc.set_lon("1.2");
    loc.set_lat("3.4");
    REQUIRE(loc.lon() == Approx(1.2));
    REQUIRE(loc.lat() == Approx(3.4));
}

TEST_CASE("set lon/lat from string with trailing characters") {
    osmium::Location loc;
    REQUIRE_THROWS_AS({
        loc.set_lon("1.2x");
    }, osmium::invalid_location);
    REQUIRE_THROWS_AS({
        loc.set_lat("3.4e1 ");
    }, osmium::invalid_location);
}

TEST_CASE("set lon/lat from string with trailing characters using partial") {
    osmium::Location loc;
    const char* x = "1.2x";
    const char* y = "3.4 ";
    loc.set_lon_partial(&x);
    loc.set_lat_partial(&y);
    REQUIRE(loc.lon() == Approx(1.2));
    REQUIRE(loc.lat() == Approx(3.4));
    REQUIRE(*x == 'x');
    REQUIRE(*y == ' ');
}

