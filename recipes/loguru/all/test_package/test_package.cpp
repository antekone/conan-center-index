#include <loguru.hpp>

int main(int argc, char** argv) {
    loguru::init(argc, argv);
    LOG_F(INFO, "42=={}", 42);
    LOG_F(INFO, "Use fmt? {}", LOGURU_USE_FMTLIB);
    return 0;
}

