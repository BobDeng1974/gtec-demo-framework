#ifndef PS_EMIT_GLES3_PARTICLESYSTEM_EMITCOUNTER_HPP
#define PS_EMIT_GLES3_PARTICLESYSTEM_EMITCOUNTER_HPP
/****************************************************************************************************************************************************
 * Copyright (c) 2015 Freescale Semiconductor, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *    * Redistributions of source code must retain the above copyright notice,
 *      this list of conditions and the following disclaimer.
 *
 *    * Redistributions in binary form must reproduce the above copyright notice,
 *      this list of conditions and the following disclaimer in the documentation
 *      and/or other materials provided with the distribution.
 *
 *    * Neither the name of the Freescale Semiconductor, Inc. nor the names of
 *      its contributors may be used to endorse or promote products derived from
 *      this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************************************************************************************/

#include <FslBase/BasicTypes.hpp>

namespace Fsl
{
  struct EmitCounter
  {
  private:
    uint32_t m_emitFraction{0};
    uint32_t m_count{0};

  public:
    EmitCounter() = default;

    uint32_t Count() const
    {
      return m_count;
    }


    void Update(const uint64_t millisecondsSinceLastUpdate, const uint32_t particlesPerSecond)
    {
      uint64_t limit = (static_cast<uint64_t>(particlesPerSecond) << 20);
      uint64_t particlesPerMillisecond = limit / 1000;
      uint64_t particles = particlesPerMillisecond * millisecondsSinceLastUpdate;
      particles += m_emitFraction;
      m_emitFraction = static_cast<uint32_t>(particles & 0xFFFFF);
      m_count = static_cast<uint32_t>(particles >> 20);
    }
  };
}

#endif
